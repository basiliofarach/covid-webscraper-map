from django.apps import AppConfig


class CovidMapConfig(AppConfig):
    name = 'covidMap'

    def ready(self):

        from updateMap import ScheduledUpdate
        ScheduledUpdate.start()
