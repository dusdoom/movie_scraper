import scrapy

class Movie(scrapy.Item):
    # The name of the movie
    name = scrapy.Field()
    # Year of release
    year = scrapy.Field()
    # reviews = scrapy.Field()