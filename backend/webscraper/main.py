import schedule
import time
import os
from ..app import *
import json


def recent():
    os.system('scrapy crawl MyAnimeListRecent -O ../Anirate.json')
    # 'Anirate.json' is now updated. Get the data from the file
    with open('../Anirate.json', 'r') as file:
            data = file.read()
    data = json.loads(data)
    # confirmed data is now the data.
    """Step 2:"""
    for anime in data:
        animeObj = Anime.query.filter_by(title=anime['title']).first() # NOTE: Only one should pop up #
        if animeObj: # Can be the anime OR None
            # The anime is already in the database
            """Step 4:"""
            if animeObj.cur_episode == anime['epNum']: # Episode number already matches, do not SIGNAL
                pass
            else: # Episode number does NOT match. SIGNAL
                animeObj.cur_episode=anime['epNum']
        else:
            """Step 3:"""
            # The anime is not in the database. SIGNAL
            animeObj = Anime(title=anime['title'], cur_episode=anime['epNum'])
        db.session.add(animeObj)
        db.session.commit()
    print(Anime.query.all())
    

print('Scheduler initialised')
schedule.every().day.at("11:00").do(recent)
print('Next job is set to run at: ' + str(schedule.next_run()))

while True:
    schedule.run_pending()
    time.sleep(1)