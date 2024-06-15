import scrapy

class User(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    # a list of Review Items, denormalization is fine here
    reviews = scrapy.Field()
    source = scrapy.Field()
    category = scrapy.Field()