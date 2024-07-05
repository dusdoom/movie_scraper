import json
from movie_scraper.items.movie import Movie
from movie_scraper.items.review import Review

class SaveContent:
    def open_spider(self, spider):
        self.movie_file = open('/primary/40 projects/movie_scraper/output/movies.json', 'w')
        self.review_file = open('/primary/40 projects/movie_scraper/output/reviews.json', 'w')

    def close_spider(self, spider):
        self.movie_file.close()
        self.review_file.close()

    def process_item(self, item, spider):
        if isinstance(item, Movie):
            line = json.dumps(dict(item)) + "\n"
            self.movie_file.write(line)
        elif isinstance(item, Review):
            line = json.dumps(dict(item)) + "\n"
            self.review_file.write(line)
        return item
