from django.apps import AppConfig
import time


class ClientsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clients'

    def ready(self):
        from .tasks import start
        time.sleep(2)
        start()
