import os
from pydantic import BaseModel
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_401_UNAUTHORIZED
import jwt

from utils.ExceptionWrapper import handle_request


SECRET_KEY = os.getenv("SECRET_KEY")


class SignedDetails(BaseModel):
    email: str
    first_name: str
    last_name: str
    uid: str
    user_type: str
    exp: int


def validate_token(token: str) -> SignedDetails:
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return SignedDetails(**payload)


@handle_request
class AuthenticateMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        cookie_token = request.cookies.get("auth")

        if not cookie_token:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="No auth token provided."
            )

        try:
            payload = jwt.decode(cookie_token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Token expired."
            )
        except jwt.InvalidTokenError as e:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {str(e)}"
            )

        request.state.email = payload.get("email")
        request.state.first_name = payload.get("first_name")
        request.state.last_name = payload.get("last_name")
        request.state.uid = payload.get("uid")
        request.state.user_type = payload.get("user_type")

        response = await call_next(request)
        return response
