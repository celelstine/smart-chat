from django.apps import AppConfig


class SmartChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'smart_chat'

    def ready(self):
        import smart_chat.signals.handlers  # noqa
