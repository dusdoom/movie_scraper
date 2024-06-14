# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# Specially for Movies, i should differentiate the movie yielded by the spider from the one that will be stored in the database
# This should happen because altough the movie link is unique for each website, it shouldnt be the field to identify a movie
# because that would generate a lot of duplicated data
class Movie(scrapy.Item):
    name = scrapy.Field()
    # url will only be used to identify a movie while scraping, it shouldnt be used to identify a movie in the database
    url = scrapy.Field()
    # a list of Review Items, denormalization is fine here
    reviews = scrapy.Field()

class Review(scrapy.Item):
    userUrl = scrapy.Field()
    positiveSentiment = scrapy.Field()
    movieUrl = scrapy.Field()
    rating = scrapy.Field()
    fullReviewUrl = scrapy.Field()
    description = scrapy.Field()
    date = scrapy.Field()
    # website where the review was found, this could be rotten tomatoes, imdb, metacritic, adoro cinema or letterboxd
    source = scrapy.Field()

class User(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    # a list of Review Items, denormalization is fine here
    reviews = scrapy.Field()
    source = scrapy.Field()
    category = scrapy.Field()
    
