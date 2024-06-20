import scrapy

# Specially for Movies, i should find a way todifferentiate the movie yielded by the spider from the one that will be stored in the database
# This should happen because altough the movie link is unique for each website, it shouldnt be the field to identify a movie
# because that would generate a lot of duplicated data
class Movie(scrapy.Item):
    id = scrapy.Field()
    year = scrapy.Field()
    name = scrapy.Field()
    # url will only be used to identify a movie while scraping, it shouldnt be used to identify a movie in the database
    url = scrapy.Field()
    # a list of Review Items, denormalization is fine here
    reviews = scrapy.Field()