from django.apps import AppConfig


class ImagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "images"

    def ready(self):  # Runs when the application is loaded.
        # Import signal handlers
        import images.signals
