from scrapy import Spider
from movie_scraper.items.movie import Movie
from movie_scraper.items.user import User
from movie_scraper.items.review import Review
from movie_scraper.pipelines.save_content import SaveContent
from movie_scraper.pipelines.remove_duplicate import RemoveDuplicate
import scrapy
import json

MOVIES_FILE = "/primary/60 projects/movie-scraper/movies_test.txt"

AMOUNT_OF_USERS = 50
AMOUNT_OF_REVIEWERS = 30

# currently this heavily depends on the API instead of the website itself
# it would be better to create some functions that scrape the website directly
class RottenTomatoesSpider(Spider):
    name = "rotten_tomatoes"
    allowed_domains = ["www.rottentomatoes.com"]
    custom_settings = {
        "DOWNLOAD_DELAY": "0.5",
        # "RANDOMIZE_DOWNLOAD_DELAY": "True",
        "ITEM_PIPELINES": {
            SaveContent: 300,
            RemoveDuplicate: 100,
        }
    }
    
    def start_requests(self):
        movie_names = open(MOVIES_FILE, "r").readlines()
        for line in movie_names:
            if line[0] == "#":
                continue
            movie_name = "_".join(line.strip().split(" "))
            movie_url = f"https://www.rottentomatoes.com/m/{movie_name}/reviews"

            yield scrapy.Request(movie_url, callback=self.parse)

    # Gets the API endpoint to fetch the first batch of reviewers from a movie.
    # This approach offloads the need to work with JavaScript and makes the process faster, altough it's very prune to errors.
    def parse(self, response):
        # url to load more reviews from users
        load_more_users = response.selector.xpath("//load-more-manager/@endpoint").get()
        yield scrapy.Request(f"https://www.rottentomatoes.com{load_more_users}?pageCount={AMOUNT_OF_USERS}", callback=self._get_users)


    # Generates a request for each user in the response based on the API pagination.
    def _get_users(self, response):
        response_json = json.loads(response.text)
        for review in response_json["reviews"]:
            if "criticName" not in review or "criticPageUrl" not in review:
                continue

            url = review['criticPageUrl'] if "criticPageUrl" in review else None
            name = review["criticName"] if "criticName" in review else None

            yield self._parse_user(name, url)
            yield scrapy.Request(f"https://www.rottentomatoes.com/napi{review['criticPageUrl']}/movies", callback=self._parse_reviews)

        if(response_json["pageInfo"]["hasNextPage"]):
            end_cursor = response_json["pageInfo"]["endCursor"]
            parsed_url = f"https://www.rottentomatoes.com{response_json["api"]}?after={end_cursor}&pageCount={AMOUNT_OF_REVIEWERS}"
            yield scrapy.Request(parsed_url, callback=self._get_users)

    # Builds and yield a Movie item.
    def _parse_movie(self, name, url, year):
        movie = Movie()
        movie["name"] = name
        movie["id"] = url
        movie["year"] = year
        movie["url"] = url
        return movie


    # Builds and yield a User item.
    def _parse_user(self, name, url):
        user = User()
        user["name"] = name
        user["id"] = url
        user["url"] = f'www.rottentomatoes.com{url}'
        user["source"] = "www.rottentomatoes.com"
        # this should be properly handled as soon as audience is implemented
        user["category"] = "critic" in url and "critic" or "audience"
        return user

    # Builds and yield multiple Review items for each user.
    def _parse_reviews(self, response):
        response_json = json.loads(response.text)

        user_name = response_json["vanity"]
        user_url = f"https://www.rottentomatoes.com/critics/{user_name}"

        for review in response_json["reviews"]:
            if "mediaTitle" not in review or "mediaInfo" not in review:
                continue
            
            yield self._parse_movie(review["mediaTitle"], review["mediaUrl"], review["mediaInfo"])

            review_item = Review()
            review_item["userUrl"] = user_url
            review_item["positiveSentiment"] = review["tomatometerState"] == "fresh" 
            review_item["source"] = "www.rottentomatoes.com"
            review_item["date"] = review["date"]
            review_item["fullReviewUrl"] = review["url"] if "url" in review else None
            review_item["movieUrl"] = f'www.rottentomatoes.com{review["mediaUrl"]}'
            review_item["rating"] = review["originalScore"] if "originalScore" in review else None
            review_item["description"] = review["quote"]
            review_item["id"] = user_name + review["mediaUrl"]

            yield review_item
