from django.apps import AppConfig


class AppCartsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_carts'

    def ready(self):
        import app_carts.signals  # Signalsni yuklang
