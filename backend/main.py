from flask import Flask
from flask_restful import Resource, Api
import json
from flask_cors import CORS
import re
import schedule
import time
from flask_sqlalchemy import SQLAlchemy
from webscraper.Anirate.spiders.MyAnimeList import *


app = Flask('AnirateAPI')
CORS(app)
api = Api(app)
with open('backend/webscraper/watchingZirolet.json', 'r') as file:
    data = file.read()
data = json.loads(data)
data = data[0]['data']

db = SQLAlchemy(app)



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
        print(data.count('"anime_title"')) #This is correct
        reg = re.compile(r'"anime_title":"(.*?)"')
        titles = reg.findall(data)
        reg = re.compile(r'"anime_image_path":"(.*?)"')
        srcs = reg.findall(data)
        for i in range(len(srcs)):
            srcs[i] = srcs[i].replace('\\', '')
        return [{'title': title, 'src': src} for title, src in zip(titles, srcs)]
api.add_resource(Watching, '/watching/<username>')
    

def recentJob(t):
    print("Checking for the latest episodes...")
    #Needs to rerun the RecentSpider spider:
    process = CrawlerProcess()
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
    schedule.every().day.at("01:00").do(recentJob,"Something")
    app.run()