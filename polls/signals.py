# polls/signals.py

from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
import logging
from .utils import get_client_ip


logger = logging.getLogger('myapp')


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip_address = get_client_ip(request)
    logger.info(f"User {user.username} logged in from IP address {ip_address}.")


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    ip_address = get_client_ip(request)
    logger.info(f"User {user.username} logged out from IP address {ip_address}.")


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    ip_address = get_client_ip(request)
    username = credentials.get('username', 'Unknown')
    logger.warning(f"Login failed for username {username} from IP address {ip_address}.")
