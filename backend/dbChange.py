from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from app import *

drStone = Anime.query.filter_by(title='Dr. Stone: New World').first()
vinSaga = Anime.query.filter_by(title='Vinland Saga Season 2').first()
print(drStone)
print(drStone.cur_episode)
print('Vin Saga Ep:', vinSaga.cur_episode)
drStone.cur_episode = 0
vinSaga.cur_episode = 0
db.session.add(drStone)
db.session.add(vinSaga)
db.session.commit()
print(drStone.cur_episode)
print('Vin Saga Ep:', vinSaga.cur_episode)