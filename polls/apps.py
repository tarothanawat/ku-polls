"""Used for logging and configuring the 'polls' application."""

from django.apps import AppConfig


class PollsConfig(AppConfig):
    """Configuration class for the 'polls' app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'

    def ready(self):
        """Import signal handlers when the app is ready."""
        import polls.signals
