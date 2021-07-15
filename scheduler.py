import datetime
from application.spotify_requests import discover_weekly
   

if __name__ == "__main__":
    #date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    discover_weekly.weekly_scheduler()