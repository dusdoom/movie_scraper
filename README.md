# Movie review scraper
## About
A very rough code for a webscraper made with the intent of building a dataset of movie reviews from multiple sources to be used in multiple smaller projects, mainly a **movie recommendation system**. Each spider should be given a list of url or implement it's own URL builder function that will scrape data based on a predefined flow, parsing all the reviews to the same format.
  
## Documentation
This documentation should contain resources generic enough to implement the same spider on most review websites using any library, framework, language or tool. For my case, i choose to use the Scrapy framework.
### Scraping flow
The **flowchart** bellow is supposed to represent the process for each movie and should be compatible with most website review structure. This does not mean that a spider should be responsible for every website (which should be pretty complex to do) but declares a step-by-step to be performed on each one.

![scraping flowchart](https://raw.githubusercontent.com/dusdoom/movie_scraper/main/docs/scraping_flow.svg?token=GHSAT0AAAAAACU5GR2GIECE3I4OP7Y6YIJ2ZUWJNKQ)

>  "**Top user**" should be a definition of how prestigious is the user as a movie reviewer. Each source should have it's own algorithm to determine this. While this could mean being a Top Critic in Rotten Tomatoes, it could be a user with more than 200 reviews in AdoroCinema.
>  Altough this process seems to be part of the **cleaning process**, defining top users during the scraping stage helps to prevent unnecessary pages to be parsed, speeding up the process and saving some bandwich.

### Data structure
This is supposed to represent the data scrapped, focusing solely on the the reviews and users. Later on, this could be incremented with movie metadatas from a open source API or be stored in a database with `movieName_releaseDate` as a ID, for example.

| Field             | Description                                                                                   |
|-------------------|-----------------------------------------------------------------------------------------------|
| sentiment         | The sentiment of the review text(positive, negative). Most times this will be based on the rating|
| userUrl           | The URL of the user who wrote the review                                                       |
| movieName         | The name of the movie                                                                          |
| movieYear         | Release year of the movie                                                                      |
| rating            | Unparsed rating from the review (e.g. 8.5/10, 4/5, A+, C.)                                     |
| text              | The review text                                                                                |
| userName          | The user name                                                                                  |
| isRelevantRating  | Checks if the review is highly relevant to the movie, e.g. a review from a top critic or has multiple likes |
| source            | The source of the review (e.g. IMDB, Rotten Tomatoes, etc.)                                    |

