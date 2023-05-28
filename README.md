# **An episode will not work in the "Watching" tab if the CONSUMET API cannot find that specific anime. The "Recents" tab works better**

# Running the Anirate Program
1. Start a virtual environment in parent "Anirate" directory.
2. Now install dependencies in the parent "Anirate" directory with:
    $ pip install -r requirements.txt
3. Run the Flask Web Server in the "backend" directory with:
    $ python app.py
4. Run the recent anime update Scraper by opening ANOTHER terminal (in same venv) and running this command in the parent "Anirate" directory:
    $ python -m backend.webscraper.main
5. Start ANOTHER terminal (in same venv) and run this command in "Anirate" directory to start the ScrapyRT Web Server:
    $ scrapyrt
5. Run the react server by opening another terminal and running these commands in the "frontend" directory (Will start on Port 3000):
    $ npm install --force
    $ npm start
6. Pull and run the Docker image for the *consumet-api* to allow anime streaming (Make sure Docker Desktop is running. React will be on Port 3000):
    $ docker pull riimuru/consumet-api
    $ docker run -p 3500:3000 riimuru/consumet-api

# How to use the Anirate Program
1. Sign up for an account, ensuring that your username is the same as your username in "MyAnimeList", then login with that account.
2. On every hard refresh, you will get a notification if a new episode is released that is on your "Watching" list.
3. You can click on an anime in the "Recents" or "Watching" link to watch the episode if it is available on the the streaming platform!