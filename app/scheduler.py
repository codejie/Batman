from apscheduler.schedulers.background import BackgroundScheduler

class Scheduler():
    def __init__(self):
        self.__scheduler = BackgroundScheduler()

    def start(self):
        self.__scheduler.start()

    def shutdown(self):
        self.__scheduler.shutdown(True)

    def addJob(self, **kwargs):
        self.__scheduler.add_job()

    def removeJob(self, name: str):
        pass

scheduler = Scheduler()

