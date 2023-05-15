from flask import Flask, Response
from flask_restful import Resource, Api
import json
from flask_cors import CORS
import sqlalchemy
import requests
from flask_sqlalchemy import SQLAlchemy

app = Flask('AnirateAPI')
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(200))
    email = db.Column(db.String(200))

    def __init__(self, username, email,):
        self.username = username


class Recent(Resource):
    #How can I run the "RecentSpider" once a day at a certain time
    def get(self):
        with open('backend/Anirate.json', 'r') as file:
            data = file.read()
        data = json.loads(data)
        return data
api.add_resource(Recent, '/recents')

    
class Watching(Resource): #Must implement webscraper here, in order to pass username to URL

    def get(self, username):
        resp = requests.get('http://localhost:9080/crawl.json?spider_name=MALWatching&start_requests=true')
        data = resp.json()['items']
        print(data)
        #Set database up now:
        """
        1. In the database, get the current user and their "Watching" list
        2. Delete all of their list
        3. Immediately after, set this new "watching" list to belong to the user.
        """
        return Response(
            resp.text, status=resp.status_code, content_type=resp.headers['content-type'],
        )

api.add_resource(Watching, '/watching/<username>')
    

def recentJob(t):
    #This runs once a day, at the same time the WebScraper runs
    signedIn = False
    if signedIn:
        print("Checking for the latest episodes...")
        #Once the update occured and the file is changed, we must check:
            #If any of the anime's that is in the json e.x. {title: "Mashle"...,} are in the user's
            #"watching" list that is part of the database of Flask.
        pass




if __name__ == '__main__':
    db.create_all()
    app.run()