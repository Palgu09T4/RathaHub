from django.apps import AppConfig
from django.apps import AppConfig
from django.db.backends.signals import connection_created
class AccountConfig(AppConfig):
    name = 'account'

    def ready(self):
        # Import signals inside ready()
        pass

    def ready(self):
        def enable_foreign_keys(sender, connection, **kwargs):
            if connection.vendor == 'sqlite':
                cursor = connection.cursor()
                cursor.execute('PRAGMA foreign_keys = ON;')

        connection_created.connect(enable_foreign_keys)

