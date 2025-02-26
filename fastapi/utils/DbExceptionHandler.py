import functools
import logging

from sqlalchemy.exc import DataError, IntegrityError, OperationalError
from utils.AppError import AppError

logger = logging.getLogger(__name__)


def handle_db_exceptions(component: str):
    """Decorator to catch, log, and handle exceptions in service functions"""

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)

            except AppError as ae:
                logger.error(
                    f"AppError in {component}: {ae.message}, Exception: {ae.exception}"
                )
                raise ae  # Pass to FastAPI's global exception handler

            except IntegrityError as ie:
                logger.error(f"Database integrity error in {component}: {str(ie)}")
                raise AppError(
                    status_code=400,
                    component=component,
                    message="Database integrity constraint violated",
                    exception=ie,
                )

            except OperationalError as oe:
                logger.error(f"Database operation error in {component}: {str(oe)}")
                raise AppError(
                    status_code=500,
                    component=component,
                    message="Database operation failed",
                    exception=oe,
                )

            except (
                DataError
            ) as de:  # Handles invalid data types (e.g., inserting string in an int column)
                logger.error(f"Invalid data error in {component}: {str(de)}")
                raise AppError(
                    status_code=422,
                    component=component,
                    message="Invalid data provided",
                    exception=de,
                )

            except TimeoutError as te:  # Handles timeouts in async operations
                logger.error(f"Request timeout in {component}: {str(te)}")
                raise AppError(
                    status_code=504,
                    component=component,
                    message="Request timed out",
                    exception=te,
                )

            except Exception as e:
                logger.error(f"Unexpected error in {component}: {str(e)}")
                raise AppError(
                    status_code=500,
                    component=component,
                    message="Unexpected error occurred",
                    exception=e,
                )

        return wrapper

    return decorator
