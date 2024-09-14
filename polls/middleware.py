"""Logger for failed user login attempts."""
from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger('myapp')


class FailedLoginLoggerMiddleware(MiddlewareMixin):
    """Logger for failed user login attempts."""

    def process_exception(self, request, exception):
        """Logger for failed user login attempts."""
        if isinstance(exception, ValueError):
            logger.warning(f"Failed login attempt from IP: {request.META.get('REMOTE_ADDR')}")
        return None
