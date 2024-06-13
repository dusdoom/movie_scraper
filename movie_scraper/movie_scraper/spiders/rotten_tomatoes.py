from scrapy import Spider
from movie_scraper.items import Movie, Review, Critic
import scrapy
import json

MOVIES_FILE = "/primary/60 projects/movie-scraper/movies_test.txt"

AMOUNT_OF_REVIEWERS = 556

# currently this heavily depends on the API instead of the website itself
# that means that if the API changes, this spider will break i more work should be done
# it would be better to create some functions that scrape the website directly
class RottenTomatoesSpider(Spider):
    name = "rotten_tomatoes"
    allowed_domains = ["www.rottentomatoes.com"]
    custom_settings = {
        "DOWNLOAD_DELAY": "0.5",
        "RANDOMIZE_DOWNLOAD_DELAY": "True",
        "CONCURRENT_REQUESTS": "16",
        "RANDOM_UA_PER_PROXY": True,
    }
    
    def start_requests(self):
        movie_names = open(MOVIES_FILE, "r").readlines()
        for line in movie_names:
            if line[0] == "#":
                continue
            movie_name = "_".join(line.strip().split(" "))
            movie_url = f"https://www.rottentomatoes.com/m/{movie_name}/reviews"

            yield scrapy.Request(movie_url, callback=self.parse)

    def parse(self, response):
        # url to load reviews from critics
        load_more_critics = response.selector.xpath("//load-more-manager/@endpoint").get()
        yield scrapy.Request(f"https://www.rottentomatoes.com{load_more_critics}?pageCount={AMOUNT_OF_REVIEWERS}", callback=self._get_critic_pages)

    def _get_critic_pages(self, response):
        response_json = json.loads(response.text)

        for review in response_json["reviews"]:
            yield scrapy.Request(f"https://www.rottentomatoes.com/{review['criticPageUrl']}", callback=self._get_critic_reviews)

    def _get_critic_reviews(self, response):
        critic = Critic()
        # it's -2 because the website adds /movies at the end of the url
        name = response.url.split("/")[-2]
        url = response.url

        yield scrapy.Request(f"https://www.rottentomatoes.com/napi/critics/{name}/movies", callback=self._parse_reviews)


    def _parse_reviews(self, response):
        response_json = json.loads(response.text)

        critic_name = response.url.split("/")[-2]
        critic_url = f"https://www.rottentomatoes.com/{critic_name}"

        for review in response_json["reviews"]:
            review_item = Review()
            review_item["criticUrl"] = critic_url
            review_item["positiveSentiment"] = review["tomatometerState"] == "fresh" 
            review_item["source"] = "www.rottentomatoes.com"
            review_item["date"] = review["date"]
            review_item["criticName"] = critic_name
            review_item["fullReviewUrl"] = review["url"] if "url" in review else None
            review_item["movieUrl"] = review["mediaUrl"]
            review_item["rating"] = review["originalScore"] if "originalScore" in review else None
            review_item["description"] = review["quote"]

            yield review_item
