from scrapy.exceptions import DropItem
from scrapy import Item
from movie_scraper.items.movie import Movie
from movie_scraper.items.review import Review
from itemadapter import is_item, ItemAdapter
from sys import getsizeof

import json


class RottenTomatoesPipeline:
    def __init__(self):
        self.items_parsed = set()
        self.unique_users = set()
        self.user_file = open('/primary/40 projects/movie_scraper/output/users.json', 'w')

    def process_item(self, item, spider):
        # Every item should be unique
        self.remove_duplicate(item)

        if isinstance(item, Movie):
            item = self.process_movie(item)
        elif isinstance(item, Review):
            item = self.process_review(item)
        else:
            raise DropItem(f"Unknown item type: {item}")

        return item

    def process_movie(self, item):
        # Parses year to int
        try:
            item['year'] = int(item['year'])
        except:
            raise DropItem(f"Year {item['year']} cannot be parsed")
        
        # Lowercases movie name
        item['name'] = item['name'].lower()

        return item

    def process_review(self, item):
        # Lowercases movieId
        item["movieId"] = item["movieId"].lower()
        # TODO: create rating parsing algorithm using linear interpolation

        # Parses user name from 'user-name' to 'user name'
        item['userName'] = " ".join(item['userName'].split("-")).lower()
    
        # Checks if user is unique
        if item['userName'] not in self.unique_users:
            self.unique_users.add(item['userName'])

        return item
   
    def remove_duplicate(self, item):
        if str(item) in self.items_parsed:
            raise DropItem(f"Duplicated item: {str(item)}")

        self.items_parsed.add(str(item))
        return item

    def close_spider(self, spider):
        print(f"Unique users: {len(self.unique_users)}")
        print(self.unique_users)
        print(f"Unique items: {len(self.items_parsed)}")
        print(f"Memory usage: {getsizeof(self.items_parsed)}")
        return