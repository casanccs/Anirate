from flask import Flask
from flask_restful import Resource, Api
import json
from flask_cors import CORS
import re
import schedule
import time
import sqlalchemy
from webscraper.Anirate.spiders.MyAnimeList import *
from twisted.internet import reactor


app = Flask('AnirateAPI')
CORS(app)
api = Api(app)
with open('backend/webscraper/watchingZirolet.json', 'r') as file:
    data = file.read()
data = json.loads(data)
data = data[0]['data']




class Recent(Resource):
    #How can I run the "RecentSpider" once a day at a certain time
    def get(self):
        with open('backend/webscraper/Anirate/Anirate.json', 'r') as file:
            data = file.read()
        data = json.loads(data)
        return data
api.add_resource(Recent, '/recents')

    
class Watching(Resource): #Must implement webscraper here, in order to pass username to URL

    def get(self, username):
        #The idea is I want to run the spider and redo this
        """
        The issue is that all the data is in a huge ugly string. I need to be able parse the string.
        1. Get: "anime_title":"Jigokuraku",
        2. Get: "anime_image_path":"https:\/\/cdn.....", Yes get rid of the backward slashes
        """
        runner = CrawlerRunner(settings = {
            "FEEDS":{
                f'backend/webscraper/Anirate/watchingStore/{username}.json': {'format': 'json'}
            }
        })
        d = runner.crawl(MyAnimeListWatchingSpider, start_urls=[f'https://myanimelist.net/animelist/{username}?status=1'])
        reactor.run()
        d.addBoth(lambda _: reactor.stop())
        #Now the file with the username would be updated everytime they go to this link
        with open(f'backend/webscraper/Anirate/watchingStore/{username}.json','r') as file:
            data = file.read()
        data = json.loads(data)
        return data
api.add_resource(Watching, '/watching/<username>')
    

def recentJob(t):
    print("Checking for the latest episodes...")
    #Needs to rerun the RecentSpider spider:
    process = CrawlerProcess(settings = {
        "FEEDS":{
            'backend/webscraper/Anirate/Anirate.json': {
                'format': 'json',
                'overwrite': 'True',
            }
        }
    })
    process.crawl(MyAnimeListRecentSpider)
    process.start()
    #At this point, the 'Anirate.json' file is updated
    #Done!
    signedIn = False
    if signedIn:
        #Once the update occured and the file is changed, we must check:
            #If any of the anime's that is in the json e.x. {title: "Mashle"...,} are in the user's
            #"watching" list that is part of the database of Flask.
        pass




if __name__ == '__main__':
    recentJob('Something')
    schedule.every().day.at("01:00").do(recentJob,"Something")
    app.run()