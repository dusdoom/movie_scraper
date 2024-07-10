from scrapy.exceptions import DropItem
from scrapy import Item
from movie_scraper.items import Review
from itemadapter import is_item, ItemAdapter
from sys import getsizeof
from pathlib import Path
from movie_scraper.settings import ROOT_DIR
import os
import json

class RottenTomatoesPipeline:
    def __init__(self):
        self.movies_parsed = set()
        self.users_parsed = set()

    def process_item(self, item, spider):
        self._add_to_counter(item)
        item = self._parse_user_name(item)
        item = self._parse_movie_year(item)

        return item

    def _add_to_counter(self, item):
        movie_year_name = f'[{item["movieYear"]}]{item["movieName"]}'
        user_url = f'{item["userUrl"]}'

        if movie_year_name not in self.movies_parsed:
            self.movies_parsed.add(movie_year_name)
        if user_url not in self.users_parsed:
            self.users_parsed.add(user_url)

    def _parse_user_name(self, item):
        user_name = item.get("userName")
        # capitalize the user name
        if user_name:
            item["userName"] = item["userName"].replace("-", " ").title()

        return item

    def _parse_movie_year(self, item):
        try:
            item["movieYear"] = int(item["movieYear"])
        except ValueError:
            raise DropItem(f"Movie year {movie_year} is not a valid year.")

        return item
    def close_spider(self, spider):
        print(f"Movies parsed from rotten tomatoes: {len(self.movies_parsed)}")
        print(f"Users parsed from rotten tomatoes: {len(self.users_parsed)}")
        
        return

class RatingNormalization:
    alphanumeric_scale = {
        "A+": (92, 100), "A": (85, 91), "A-": (80, 85),
        "B+": (75, 79), "B": (70, 74), "B-": (70, 75),
        "C+": (65, 70), "C": (60, 65), "C-": (55, 60),
        "D+": (50, 55), "D": (45, 50), "D-": (40, 45),
        "F": (0, 40)
    }

    numeric_scale = {
        "3": {0: (0, 10), 1: (0, 50), 2: (50, 100), 3: (100, 100)},
        "4": {0: (0, 10), 1: (0, 33.33), 2: (33.33, 66.67), 3: (66.67, 100), 4: (100, 100)},
        "5": {0: (0, 10), 1: (0, 25), 2: (25, 50), 3: (50, 75), 4: (75, 100), 5: (100, 100)},
        "10": {
            0: (0, 1), 1: (0, 10), 2: (10, 20), 3: (20, 30),
            4: (30, 40), 5: (40, 50), 6: (50, 60), 7: (60, 70),
            8: (70, 80), 9: (80, 90), 10: (90, 100)
        },
    }

    def process_item(self, item, spider):
        rating = item.get("rating")
        if not rating:
            return item

        # split the rating into components and remove any leading/trailing whitespaces
        rating_components = [x.strip() for x in rating.split("/")]

        # means the rating is in the format of "rating/max_rating", e.g. "8.5/10", "4/5", "85/100"
        if len(rating_components) == 2:
            max_rating = rating_components[1]
            rating_value = float(rating_components[0])

            # if the max rating is 100, then the rating is already normalized
            if max_rating == "100":
                item["rating"] = rating_value
            else:
                try:
                    item["rating"] = self.numeric_scale[max_rating][int(rating_value)]
                except KeyError:
                    print(f"Rating {rating_components} out of scale patterns.")
        # means the rating is in the format of "A+", "B", "C-", etc
        else:
            rating_value = rating_components[0]
            try:
                item["rating"] = self.alphanumeric_scale[rating_value]
            except KeyError:
                raise DropItem(f"Rating {rating_value} out of scale patterns.")

        return item

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
        review_file_path = Path(f'{ROOT_DIR}/output/reviews.json')

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
            print(f"Parsed {item["userName"]} review to {item["movieName"]}")
        return item