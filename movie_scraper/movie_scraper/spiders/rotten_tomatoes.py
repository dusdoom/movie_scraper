from scrapy import Spider
from movie_scraper.items import Review
from movie_scraper.pipelines import RottenTomatoesPipeline, RatingNormalization, SaveContent
from movie_scraper.settings import ROOT_DIR
import scrapy
import json

MOVIES_FILE = f"{ROOT_DIR}/assets/movies.txt"

REVIEWERS_PER_PAGE = 20
REVIEWS_PER_PAGE = 20
MIN_REVIEW_COUNT = 20


class RottenTomatoesSpider(Spider):
    name = "rotten_tomatoes"
    allowed_domains = ["www.rottentomatoes.com"]
    custom_settings = {
        "DOWNLOAD_DELAY": "0.5",
        # "RANDOMIZE_DOWNLOAD_DELAY": "True",
        "ITEM_PIPELINES": {
            RottenTomatoesPipeline: 100,
            RatingNormalization: 901,
            SaveContent: 902,
        }
    }

    scraped_users = []

    def start_requests(self):
        movie_names = open(MOVIES_FILE, "r").readlines()
        for line in movie_names:
            if line[0] == "#":
                continue
            movie_name = "_".join(line.strip().split(" "))
            movie_url = f"https://www.rottentomatoes.com/m/{movie_name}/reviews"

            yield scrapy.Request(movie_url, callback=self.parse)

    # parses first batch of scraped_users
    def parse(self, response):
        users_api_endpoint = response.selector.xpath("//load-more-manager/@endpoint").get()
        api_url = f"https://www.rottentomatoes.com{users_api_endpoint}?pageCount={REVIEWERS_PER_PAGE}"
        yield scrapy.Request(api_url, callback=self.filter_out_scraped_users)

    def filter_out_scraped_users(self, response):
        # response example: https://www.rottentomatoes.com/napi/movie/d088c6b6-1f9c-31a1-8967-80ebfc401311/reviews/all
        response_json = json.loads(response.text)

        for review in response_json["reviews"]:
            # skips reviews without a user page
            if review["criticPageUrl"] is None:
                continue

            # skips scraped users
            if review["criticPageUrl"] not in self.scraped_users:
                print(f'AQUIIIIIIIIIIIIIIIIIIIIIII {response.url}')
                user_page_url = f"https://www.rottentomatoes.com/napi{review['criticPageUrl']}/movies"
                yield scrapy.Request(
                    url=user_page_url,
                    callback=self.validate_user,
                    meta={"is_top_user": review["isTopCritic"]}
                )
                self.scraped_users.append(review["criticPageUrl"])

        # handles pagination
        page_info = response_json["pageInfo"]
        if page_info["hasNextPage"]:
            base_url = f"https://www.rottentomatoes.com{response_json["api"]}"
            pagination_options = f"?after={page_info['endCursor']}&pageCount={REVIEWERS_PER_PAGE}"
            parsed_url = f"{base_url}{pagination_options}"
            yield scrapy.Request(parsed_url, callback=self.filter_out_scraped_users)

    def validate_user(self, response):
        # response example: https://www.rottentomatoes.com/napi/critics/cameron-meier/movies
        response_json = json.loads(response.text)

        # if is top user, flag it and parse reviews
        if response.meta["is_top_user"]:
            return self.parse_user_reviews(response_json, True)
        # if it has at least N reviews, flag as not top user and parse reviews
        elif len(response_json["reviews"]) >= MIN_REVIEW_COUNT:
            return self.parse_user_reviews(response_json, False)
        # if not in any of the above cases, ignores it
        else:
            print(f"User {response_json['vanity']} has less than {MIN_REVIEW_COUNT} reviews")
            return None

        return self.parse_user_reviews(response_json, False)

    def parse_user_reviews(self, response_json, is_top_user):
        user_name = response_json["vanity"]
        user_url = f"https://www.rottentomatoes.com/critics/{user_name}/movies"

        for review in response_json["reviews"]:
            # some reviews dont include the title or the info of the movie, which makes them useless
            if "mediaTitle" not in review or "mediaInfo" not in review:
                continue

            review_item = Review()
            review_item["userUrl"] = user_url
            review_item["movieName"] = review["mediaTitle"]
            review_item["movieYear"] = review["mediaInfo"]
            review_item["sentiment"] = review["tomatometerSentiment"]
            review_item["source"] = "rottentomatoes"
            review_item["rating"] = review["originalScore"] if "originalScore" in review else None
            review_item["text"] = review["quote"]
            review_item["userName"] = user_name
            review_item["isRelevantRating"] = is_top_user
            yield review_item

            # this calls a validation for a user that was already validated
            # its kinda ugly but it just works and the downside seems to be very minimal
            if response_json["pageInfo"]["hasNextPage"]:
                base_url = f"https://www.rottentomatoes.com{response_json["api"]}"
                pagination_options = f"?after={response_json['pageInfo']['endCursor']}&pageCount={REVIEWS_PER_PAGE}"
                parsed_url = f"{base_url}{pagination_options}"

                yield scrapy.Request(
                    url=parsed_url,
                    callback=self.validate_user,
                    meta={"is_top_user": is_top_user}
                )
