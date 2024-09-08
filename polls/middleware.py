from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger('myapp')


class FailedLoginLoggerMiddleware(MiddlewareMixin):

    def process_exception(self, request, exception):
        if isinstance(exception, ValueError):
            logger.warning(f"Failed login attempt from IP: {request.META.get('REMOTE_ADDR')}")
        return None