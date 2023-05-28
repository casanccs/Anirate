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

def signal(animeObj, user):
    """
        Because animeObj has a Many-To-Many relationship with User, we have a list of all the users who are watching this anime currently.
        So we can signal to each user individually by using a for loop.
    """ 
    if animeObj in user.watching:
        print(f'{user.username}: {animeObj.title} release Episode {animeObj.cur_episode} !!')
        return True
    return False


def recent(user):
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
    with open('Anirate.json', 'r') as file:
            data = file.read()
    data = json.loads(data)
    # confirmed data is now the data.
    """Step 2:"""
    for anime in data:
        anime['notificate'] = False #Make new key,value for that Anime's dictionary
        animeObj = Anime.query.filter_by(title=anime['title']).first() # NOTE: Only one should pop up #
        if animeObj: # Can be the anime OR None
            # The anime is already in the database
            """Step 4:"""
            if animeObj.cur_episode == anime['epNum']: # Episode number already matches, do not SIGNAL
                pass
            else: # Episode number does NOT match. SIGNAL
                animeObj.cur_episode=anime['epNum']
                anime['notificate'] = signal(animeObj, user)
        else:
            """Step 3:"""
            # The anime is not in the database. SIGNAL
            animeObj = Anime(title=anime['title'], cur_episode=anime['epNum'])
            anime['notificate'] = signal(animeObj, user)
    '''
    At this point, it will return a list of dictionaries with the: {title, epNum, notificate}
    So if there were 10 new episodes in Anirate.json, the new list will be the same but with notificate tacked on.
    '''
    return data

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
    cur_episode = db.Column(db.String, default="Episode 1") # Turns out this is a String

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


class CheckNewEpisodes(Resource):

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
        # Confirmed we got the user
        return jsonify(recent(current_user)) # Remember that recent(current_user) is just the data with 'notificate' tacked on
api.add_resource(CheckNewEpisodes, '/check')



if __name__ == '__main__':
    db.create_all()
    print(User.query.all())
    app.run()