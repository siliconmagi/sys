#  import json
import scrapy


class ytUrls(scrapy.Spider):
    name = 'ytUrls'
    start_urls = [
        'https://www.youtube.com/channel/UCYb6YWTBfD0EB53shkN_6vA/videos']
