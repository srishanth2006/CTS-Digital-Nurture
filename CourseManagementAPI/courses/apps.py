from django.apps import AppConfig


class CoursesConfig(AppConfig):
    """Application configuration for the courses app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "courses"
    verbose_name = "Course Management"

    def ready(self):
        # Import signal handlers so they are registered when the app is ready.
        import courses.signals  # noqa: F401
