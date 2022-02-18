from django.apps import AppConfig


class StatisticappConfig(AppConfig):
    name = 'statisticapp'

    def ready(self):
        from . import updater
        updater.start()
