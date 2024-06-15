import json
from movie_scraper.items.movie import Movie
from movie_scraper.items.user import User
from movie_scraper.items.review import Review

class SaveContent:
    def open_spider(self, spider):
        self.movie_file = open('/primary/60 projects/movie-scraper/output/movies.json', 'w')
        self.user_file = open('/primary/60 projects/movie-scraper/output/users.json', 'w')
        self.review_file = open('/primary/60 projects/movie-scraper/output/reviews.json', 'w')

    def close_spider(self, spider):
        self.movie_file.close()
        self.user_file.close()
        self.review_file.close()

    def process_item(self, item, spider):
        if isinstance(item, Movie):
            line = json.dumps(dict(item)) + "\n"
            self.movie_file.write(line)
        elif isinstance(item, User):
            line = json.dumps(dict(item)) + "\n"
            self.user_file.write(line)
        elif isinstance(item, Review):
            line = json.dumps(dict(item)) + "\n"
            self.review_file.write(line)
        return item
