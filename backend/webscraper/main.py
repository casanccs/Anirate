import schedule
import time
import os
from ..app import *
import json

def signal(animeObj):
    """
        Because animeObj has a Many-To-Many relationship with User, we have a list of all the users who are watching this anime currently.
        So we can signal to each user individually by using a for loop.
    """ 
    for user in User.query.all():
        if animeObj in user.watching:
            print(f'{user.username}: {animeObj.title} release Episode {animeObj.cur_episode} !!')
            '''
            Now for the hardest part.
            I know that this user needs to receive a notification. So I must send this notification to everyone who is logged into a device AS THIS
                CURRENT USER!

            Here is a similar but simpler problem that can solve this:
            1. Someone is logged in with username A on a device.
            2. Program X sends a notification to a computer who is logged in as username A every 10 seconds.

            First Solution:
            Send HTTP request from here to 
            '''


def recent():
    #How the anime/user and notification is going to work
    """
        This all when we get the recent anime!! Which means this logic will be in the scheduler
        1. As anime gets pulled into the "Anirate.json" file:
        2. Loop through each dictionary and check to see if that anime is in the database by using the
            title key in the dictionary and title field in the model.
        3. If it is NOT in the database, add it into the database, and *SIGNAL* to everyone who has this
            anime in their "watching" list. (Will go over below) [THIS IS NOT POSSIBLE BECAUSE AN ANIME IN A "WATCHING" LIST WILL BE CREATED IN DB!]
        4. If it IS in the database, check to see if the current episode matches the one that is in
            the database. Do nothing if it matches. If it does NOT match, *SIGNAL* to everyone who has this
            anime in their "animes" list. (Will go over below)
    """
    os.system('scrapy crawl MyAnimeListRecent -O ../Anirate.json')
    """Step 1:"""
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
                signal(animeObj)
        else:
            """Step 3:"""
            # The anime is not in the database. SIGNAL
            animeObj = Anime(title=anime['title'], cur_episode=anime['epNum'])
            signal(animeObj)
        db.session.add(animeObj)
        db.session.commit()
    print(Anime.query.all())
    

print('Scheduler initialised')
schedule.every(0.05).minutes.do(recent)
print('Next job is set to run at: ' + str(schedule.next_run()))

while True:
    schedule.run_pending()
    time.sleep(1)