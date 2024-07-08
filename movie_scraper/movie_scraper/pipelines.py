from scrapy.exceptions import DropItem
from scrapy import Item
from movie_scraper.items import Review
from itemadapter import is_item, ItemAdapter
from sys import getsizeof
from pathlib import Path
import os
import json

class RottenTomatoesPipeline:
    def __init__(self):
        self.movies_parsed = set()
        self.users_parsed = set()

    def process_item(self, item, spider):
        if isinstance(item, Review):
            # item = self._parse_strings(item)
            self._add_to_counter(item)

        return item

    def _add_to_counter(self, item):
        movie_year_name = f'[{item["movieYear"]}]{item["movieName"]}'
        user_url = f'{item["userUrl"]}'

        if movie_year_name not in self.movies_parsed:
            self.movies_parsed.add(movie_year_name)
        if user_url not in self.users_parsed:
            self.users_parsed.add(user_url)

    def close_spider(self, spider):
        print(f"Movies parsed from rotten tomatoes: {len(self.movies_parsed)}")
        print(f"Users parsed from rotten tomatoes: {len(self.users_parsed)}")
        return

class SaveContent:
    # solution from https://stackoverflow.com/questions/23793987/write-a-file-to-a-directory-that-doesnt-exist
    def mkdir_p(path):
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: raise

    def open_spider(self, spider):
        current_path = os.getcwd()

        review_file_path = Path(current_path + '/output/reviews.json')

        # create the directory if it doesn't exist
        review_file_path.parent.mkdir(parents=True, exist_ok=True)

        # Open the files
        self.review_file = open(review_file_path, 'w')

    def close_spider(self, spider):
        self.review_file.close()

    def process_item(self, item, spider):
        if isinstance(item, Review):
            line = json.dumps(dict(item)) + "\n"
            self.review_file.write(line)
        return item