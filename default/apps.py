from django.apps import AppConfig


class DefaultConfig(AppConfig):
    name = 'default'
    def ready(self):
        import default.signals
        import default.tasks
