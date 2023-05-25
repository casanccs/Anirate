from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from app import *

drStone = Anime.query.filter_by(title='Dr. Stone: New World').first()
print(drStone)
print(drStone.cur_episode)
drStone.cur_episode = 0
db.session.add(drStone)
db.session.commit()
print(drStone.cur_episode)
