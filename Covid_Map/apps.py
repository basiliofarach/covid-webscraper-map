from django.apps import AppConfig


class CovidMapConfig(AppConfig):
    name = 'Covid_Map'

    def ready(self):

        from updateMap import ScheduledUpdate
        ScheduledUpdate.start()
