from django.apps import AppConfig


class AdanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adan'
    def ready(self):
        from . import signals
