import scrapy

class Review(scrapy.Item):
    # The sentiment of the review (positive, negative)
    positiveSentiment = scrapy.Field()
    # The URL of the user who wrote the review
    userUrl = scrapy.Field()
    # A unique identifier for the movie consisting in the format [year]name
    movieId = scrapy.Field()
    # The name of the movie
    movieName = scrapy.Field()
    # Release year of the movie
    movieYear = scrapy.Field()
    # Unparsed rating from the review (e.g. 8.5/10, 4/5, A+, C.)
    rating = scrapy.Field()
    # The review text
    text = scrapy.Field()
    # The user name
    userName = scrapy.Field()
    # Checks if the review is highly relevant to the movie, e.g. a review from a top critic or has multiple likes
    isRelevantRating = scrapy.Field()
    # The source of the review (e.g. IMDB, Rotten Tomatoes, etc.)
    source = scrapy.Field()