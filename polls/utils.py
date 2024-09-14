"""
polls/utils.py.

This module provides utility functions for the polls application.

Functions:
- get_client_ip: Extracts the client's IP address from the request headers.
"""


def get_client_ip(request):
    """
    Get the visitor’s IP address using request headers.

    Args:
        request: The HTTP request object.

    Returns:
        str: The client's IP address. If not available, returns 'Unknown'.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')

    # Additional security measure to ensure the IP is in valid format
    if not ip:
        ip = 'Unknown'

    return ip
