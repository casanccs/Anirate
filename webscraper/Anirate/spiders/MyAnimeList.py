from pathlib import Path
import scrapy

class MyAnimeListRecentSpider(scrapy.Spider): #This gets the list of recent episodes of anime
    name = "MyAnimeListRecent"
    start_urls = [
        'https://myanimelist.net/watch/episode', #Get all latest update episode videos
    ]

    def parse(self, response):
        for anime in response.css('div.video-list-outer-vertical'):
            yield {
                'title' : anime.css('div.video-info-title a::text').get(), #Gets anime title
                'img' : anime.css('div.episode img').xpath('@data-src').get(), #Gets the image for the anime
                'epNum' : anime.css('div.episode div.title a::text').get(), #Gets current episode
            }

class MyAnimeListWatchingSpider(scrapy.Spider):
    name = "MALWatching"
    start_urls = [
        'https://myanimelist.net/animelist/Zirolet?status=1',
    ]

    def parse(self, response): #This is complicated, because this itself returns a big json file
        yield {'data': response.css('table').xpath('@data-items').get()}