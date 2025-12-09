from django.apps import AppConfig


class HomofixAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'homofix_app'
    
    # def ready(self):
    #     import homofix_app.signals
