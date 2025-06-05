from functools import wraps

from elasticsearch import exceptions
from logger import logger
from utils.AppError import AppError

from fastapi import HTTPException


def handle_request(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        component_name = func.__name__  # Dynamically get function name

        try:
            return await func(*args, **kwargs)
        except AppError as ae:
            logger.error(
                f"AppError in {component_name}: {ae.message}, Exception: {ae.exception}"
            )
            raise ae  # Let FastAPI's global exception handler deal with it

        except HTTPException as he:
            logger.error(f"HTTPException occurred: {he.detail}")
            raise AppError.from_http_exception(he, component=component_name)

        except Exception as e:
            logger.error(f"Unexpected error in {component_name}: {str(e)}")
            raise AppError(
                status_code=500,
                component=component_name,  # Dynamically set component name
                message="Unexpected error occurred",
                exception=e,
            )

        except exceptions.ConnectionError as ce:
            logger.error(f"Unexpected error in {component_name}: {str(ce)}")
            raise AppError(
                status_code=500,
                component=component_name,  # Dynamically set component name
                message="Unexpected error occurred from elastic search",
                exception=ce,
            )

        except exceptions.TransportError as e:
            logger.error(f"Unexpected error in {component_name}: {str(e)}")
            raise AppError(
                status_code=500,
                component=component_name,  # Dynamically set component name
                message="Unexpected error occurred from elastic search",
                exception=e,
            )

    return wrapper
