# polls/signals.py

"""
This module contains signal handlers for user login and logout events.
"""

from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
import logging
from .utils import get_client_ip

logger = logging.getLogger('myapp')


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """
    Signal handler for user login event.

    Logs a message when a user successfully logs in. Includes the user's
    username and the IP address from which the login attempt was made.

    Args:
        sender: The sender of the signal.
        request: The HTTP request object.
        user: The user who has logged in.
        **kwargs: Additional keyword arguments.
    """
    ip_address = get_client_ip(request)
    logger.info(f"User {user.username} logged in from IP address {ip_address}.")


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    """
    Signal handler for user logout event.

    Logs a message when a user logs out. Includes the user's username and
    the IP address from which the logout attempt was made.

    Args:
        sender: The sender of the signal.
        request: The HTTP request object.
        user: The user who has logged out.
        **kwargs: Additional keyword arguments.
    """
    ip_address = get_client_ip(request)
    logger.info(f"User {user.username} logged out from IP address {ip_address}.")


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    """
    Signal handler for user login failed event.

    Logs a message when a login attempt fails. Includes the username and
    the IP address from which the login attempt was made.

    Args:
        sender: The sender of the signal.
        credentials: The credentials used for the login attempt.
        request: The HTTP request object.
        **kwargs: Additional keyword arguments.
    """
    ip_address = get_client_ip(request)
    username = credentials.get('username', 'Unknown')
    logger.warning(f"Login failed for username {username} from IP address {ip_address}.")
