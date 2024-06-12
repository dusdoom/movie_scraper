from scrapy import Spider

class RottenTomatoesSpider(Spider):
    name = "rotten_tomatoes"
    allowed_domains = ["www.rottentomatoes.com"]
    start_urls = ["https://www.rottentomatoes.com"]

    # i dont need to yield everything? i can just return the items
    def start_requests(self):
        # read movie names from a file
        # build a link from the movie name
        # yield requests
        pass

    def parse(self, response):
        # start on movie page
        # call _extract_movie_from_its_page
        # visit critics page
        # extract all links from all critics
        ### extract 1000 links from all audience ???
        # yield iterable of requests using both links with with follow_all and _parse_critic_page
        print("Parsing Rotten Tomatoes")

    def _parse_critic_page(self, response):
        # iterate through all critics
            # extract critic item using _extract_critic
            # extract movie item using _extract_movie_from_critic_page
            # extract review item using _extract_review
            # add critic and movie to review
            # yield review
            ## review should NOT have its own table/collection
            ## this should allow me to develop a pipeline where movie and critic would have their own reference to review while yielding just one item
        print("Handling movies")
    
    def _extract_movie_from_critic_page(self, response):
        # extract information from movie page
        # return item
        print("Parsing movie")

    def _extract_critic(self, response):
        # extract information from critic page
        # return item
        print("Parsing critic")

    def _extract_review(self, response):
        # extract information from critic page
        # return item
        print("Parsing critic")

    def _extract_movie_from_its_page(self, response):
        # extract information from movie page
        # return item
        print("Parsing movie")