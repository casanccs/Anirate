from flask import Flask, Response, request, abort, jsonify
from flask_restful import Resource, Api
import json
from flask_cors import CORS, cross_origin
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import jwt
import datetime
from sqlalchemy.orm import relationship, backref



app = Flask('AnirateAPI')
CORS(app,resources={r"/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hi'
api = Api(app)
app.app_context().push()
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class Watching(db.Model):
    __table__ = 'watchings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    anime_id = db.Column(db.Integer, db.ForeignKey('animes.id'))

    user = relationship('User', backref=backref("watchings", cascade="all, delete-orphan"))
    anime = relationship('Anime', backref=backref("watchings", cascade="all, delete-orphan"))

class User(db.Model):
    __table__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)

    animes = relationship('Anime', secondary=Watching, backref='watchers')


class Anime(db.Model):
    __table__ = 'animes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    profiles = db.Column(db.Fo)
    cur_episode = db.Column(db.Integer)

#How the anime/user and notification is going to work
"""
    This all when we get the recent anime!! Which means this logic will be in the scheduler
    1. As anime gets pulled into the "Anirate.json" file:
    2. Loop through each dictionary and check to see if that anime is in the database by using the
        title key in the dictionary and title field in the model.
    3. If it is NOT in the database, add it into the database, and *SIGNAL* to everyone who has this
        anime in their "animes" list. (Will go over below)
    4. If it IS in the database, check to see if the current episode matches the one that is in
        the database. Do nothing if it matches. If it does NOT match, *SIGNAL* to everyone who has this
        anime in their "animes" list. (Will go over below)
"""


class Login(Resource):
    def post(self):
        form = request.get_json()
        user = User.query.filter_by(username=form['username']).first()
        if user and bcrypt.check_password_hash(user.password, form['password']):
            token = jwt.encode({'username': form['username'], 'exp': datetime.datetime.utcnow() + 
                                datetime.timedelta(hours=60)}, app.config['SECRET_KEY'])
            print(token)
            print(jwt.decode(token, app.config['SECRET_KEY'], 'HS256'))
            return jsonify({'token': token})
        else:
            return jsonify({'error': "Incorrect username or password"})
        
    
api.add_resource(Login, '/login')

class Logout(Resource):
    pass
api.add_resource(Logout, '/logout')

class Register(Resource):

    def post(self,):
        form = request.get_json()
        print(form)
        hashed_password = bcrypt.generate_password_hash(form['password'])
        if User.query.filter_by(username=form['username']).first(): #Confirmed working
            abort(400)
        new_user = User(username=form['username'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        print("Successful!")
        return Response(json.dumps({'data': "Created"}))
api.add_resource(Register, '/register')

class Recent(Resource):
    #How can I run the "RecentSpider" once a day at a certain time
    def get(self):
        with open('Anirate.json', 'r') as file:
            data = file.read()
        data = json.loads(data)
        return data
api.add_resource(Recent, '/recents')
 
class Watching(Resource): #Must implement webscraper here, in order to pass username to URL

    @cross_origin(supports_credentials=True)
    def post(self):
        data = request.get_json()
        token = None

        try:
            token = data['token']
            print(token)
        except:
            return jsonify({'message': 'Token is missing!'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], 'HS256')
        except:
            return jsonify({'message': 'Token is invalid!'})
        current_user = User.query.filter_by(username=data['username']).first()
        print(current_user.username)
        username = current_user.username
        resp = requests.get(f'http://localhost:9080/crawl.json?spider_name=MALWatching&url=https://myanimelist.net/animelist/{username}?status=1')
        data = resp.json()['items']
        print(data)
        #Set database up now:
        """
        1. In the database, get the current user and their "Watching" list
        2. Delete all of their list
        3. Immediately after, set this new "watching" list to belong to the user.
        """
        return jsonify({'data': data, 'username': current_user.username})
    
api.add_resource(Watching, '/watching')
    

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