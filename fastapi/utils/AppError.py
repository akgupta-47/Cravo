from fastapi import HTTPException


class AppError(Exception):
    def __init__(
        self,
        status_code: int,
        component: str,
        message: str = None,
        exception: Exception = None,
    ):
        self.status_code = status_code
        self.component = component
        self.message = message or "An error occurred"
        self.exception = str(exception) if exception else "No additional details"

    def to_dict(self):
        return {
            "component": self.component,
            "message": self.message,
            "exception": self.exception,
        }

    @classmethod
    def from_http_exception(cls, http_exception: HTTPException, component: str):
        return cls(
            status_code=http_exception.status_code,
            component=component,
            message=http_exception.detail,
            exception="Handled HTTPException",
        )
