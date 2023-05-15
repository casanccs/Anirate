import schedule
import time
import os

print('Scheduler initialised')
schedule.every(0.25).minutes.do(lambda: os.system('scrapy crawl MyAnimeListRecent -O ../../backend/Anirate.json'))
print('Next job is set to run at: ' + str(schedule.next_run()))

while True:
    schedule.run_pending()
    time.sleep(1)