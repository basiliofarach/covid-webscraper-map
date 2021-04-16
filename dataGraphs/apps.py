from django.apps import AppConfig


class DatagraphsConfig(AppConfig):
    name = 'dataGraphs'

    def ready(self):

        from updateGraphs import ScheduledUpdate
        ScheduledUpdate.start()
