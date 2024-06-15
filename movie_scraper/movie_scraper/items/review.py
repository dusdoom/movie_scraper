import scrapy

class Review(scrapy.Item):
    id = scrapy.Field()
    userUrl = scrapy.Field()
    positiveSentiment = scrapy.Field()
    movieUrl = scrapy.Field()
    rating = scrapy.Field()
    fullReviewUrl = scrapy.Field()
    description = scrapy.Field()
    date = scrapy.Field()
    # website where the review was found, this could be rotten tomatoes, imdb, metacritic, adoro cinema or letterboxd
    source = scrapy.Field()