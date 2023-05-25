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
import os


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask('AnirateAPI')
CORS(app,resources={r"/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hi'
api = Api(app)
app.app_context().push()
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

user_anime = db.Table('user_anime',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('anime_id', db.Integer, db.ForeignKey('anime.id'))
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    watching = relationship('Anime', secondary=user_anime, backref='watchers')

    def __repr__(self):
        return f'<User {self.username}>'


class Anime(db.Model):
    __tablename__ = 'anime'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    cur_episode = db.Column(db.Integer, default=0) # Turns out this is a String

    def __repr__(self):
        return f'<Anime {self.title}, ep: {self.cur_episode}>'

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
        #Set database up now:
        """
        1. Get all Anime instances that are in the data
        2. Replace the {current_user}'s watching list with the Anime instances that are currently in the data
        """
        '''Step 1:'''
        aniTitles = [anime['title'] for anime in data]
        #Some Animes wont exist, must check individually!!
        for anime in aniTitles:
            if not Anime.query.filter_by(title=anime).first(): #The Anime doesn't exist
                db.session.add(Anime(title=anime)) #Only set title for now, as default for episode number is 0, should webscrape to find the latest episode
                db.session.commit()
        animes = Anime.query.filter(Anime.title.in_(aniTitles)).all()
        #Now have all Anime Instances that are in the data
        '''Step 2:'''
        current_user.watching = animes
        db.session.add(current_user)
        db.session.commit()
        print(current_user.watching)
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
    print(User.query.all())
    app.run()