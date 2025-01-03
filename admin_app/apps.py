from django.apps import AppConfig


class AdminAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_app'
    verbose_name = 'Verwaltung'  # Der Name, der im Admin-Panel angezeigt wird
