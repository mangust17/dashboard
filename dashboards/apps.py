from django.apps import AppConfig

class DashboardsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboards'

    def ready(self):
        import dashboards.dash_apps.y2y, dashboards.dash_apps.gr_big_dash
