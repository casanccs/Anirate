from pathlib import Path
import scrapy
from scrapy.crawler import CrawlerProcess
import re

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
        Path('Anirate.json').write_bytes(response.body)

class MyAnimeListWatchingSpider(scrapy.Spider):
    name = "MALWatching"
    username = 'zirolet'
    start_urls = [
        f'https://myanimelist.net/animelist/{username}?status=1',
    ]

    #Need to test this out
    def reset(self, username):
        self.username = username
        self.start_urls = [
            f'https://myanimelist.net/animelist/{username}?status=1',
        ]

    def parse(self, response): #This is complicated, because this itself returns a big json file
        data = {'data': response.css('table').xpath('@data-items').get()}
        reg = re.compile(r'"anime_title":"(.*?)"')
        titles = reg.findall(data)
        reg = re.compile(r'"anime_image_path":"(.*?)"')
        srcs = reg.findall(data)
        for i in range(len(srcs)):
            srcs[i] = srcs[i].replace('\\', '')
        yield [{'title': title, 'src': src} for title, src in zip(titles, srcs)]
        Path(f'watching{self.username}.json').write_bytes(response.body)