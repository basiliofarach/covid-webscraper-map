from apscheduler.schedulers.background import BackgroundScheduler

from updateGraphs.Graphs import graph

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(graph, 'interval', minutes=60)
    scheduler.start()
