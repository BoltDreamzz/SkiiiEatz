from django.apps import AppConfig


class SassConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sass'

    def ready(self):
        import sass.signals