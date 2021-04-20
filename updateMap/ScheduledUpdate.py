from apscheduler.schedulers.background import BackgroundScheduler

from updateMap.Map import map

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(map, 'interval', minutes=0.3)
    scheduler.start()
