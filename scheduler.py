from application.spotify_requests import discover_weekly
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon', hour=12)
def weekly_cronjob():
    discover_weekly.insert_tracks()

