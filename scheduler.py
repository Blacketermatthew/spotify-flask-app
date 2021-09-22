from pytz import HOUR
from application.models import SpotifyTracks
from apscheduler.schedulers.background import BackgroundScheduler

sched = BackgroundScheduler()

# @sched.scheduled_job('cron', day_of_week='mon', hour=12, minute=0)
@sched.scheduled_job('cron', day_of_week='wed', hour=17, minute=42)
def weekly_cronjob():
    print("Cron is now attempting to insert tracks into the database.")
    SpotifyTracks.insert_new_tracks()

sched.start()
