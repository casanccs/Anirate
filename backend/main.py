from flask import Flask
from flask_restful import Resource, Api
import json
from flask_cors import CORS
import re


app = Flask('AnirateAPI')
CORS(app)
api = Api(app)




class Recent(Resource):

    def get(self):
        with open('webscraper/Anirate/Anirate.json', 'r') as file:
            data = file.read()
        data = json.loads(data)
        return data
api.add_resource(Recent, '/recents')

    
class Watching(Resource):

    def get(self):
        with open('webscraper/watchingZirolet.json', 'r') as file:
            data = file.read()
        data = json.loads(data)
        data = data[0]['data']
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
api.add_resource(Watching, '/watching')
    


if __name__ == '__main__':
    app.run()