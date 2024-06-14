from scrapy import Item, Field
from .base_step import BaseStep
from movie_scraper.items import Review

class NormalizeRating(BaseStep):
    item_type = Review

    def execute(self, item, spider):
        item['rating'] = int(item['rating'].split('/')[0])
        return item