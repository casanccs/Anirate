from flask import Flask, Response, request
from flask_restful import Resource, Api
import json
from flask_cors import CORS
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt



app = Flask('AnirateAPI')
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hi'
api = Api(app)
app.app_context().push()
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="Login"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    print(user_id)
    user = User.query.get(int(user_id))
    print(user)
    return User.query.get(int(user_id))


class Login(Resource):
    def post(self):
        form = request.get_json()
        user = User.query.filter_by(username=form['username']).first()
        if user:
            if bcrypt.check_password_hash(user.password, form['password']):
                db.session.add(user)
                db.session.commit()
                login_user(user, force=True, remember=True)
                print(current_user)
                return Response(json.dumps({'data': "Successful"}))
api.add_resource(Login, '/login')

class Logout(Resource):
    def get(self):
        user = current_user
        db.session.add(user)
        db.session.commit()
        logout_user()
        print("Successfully logged out")
api.add_resource(Logout, '/logout')


class Register(Resource):

    def post(self,):
        form = request.get_json()
        print(form)
        hashed_password = bcrypt.generate_password_hash(form['password'])
        new_user = User(username=form['username'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        print("Successful!")
        return Response(json.dumps({'data': "Created"}))
api.add_resource(Register, '/register')


class Recent(Resource):
    #How can I run the "RecentSpider" once a day at a certain time
    def get(self):
        print(current_user)
        with open('Anirate.json', 'r') as file:
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