from requests import get
from bs4 import BeautifulSoup
from time import sleep ,time
from random import randint
from warnings import warn
from IPython.core.display import clear_output
import pandas as pd

# Lists to store the scraped data in
names = []
years = []
imdb_ratings = []
metascores = []
votes = []
genres = []

pages = [str(i) for i in range(1,5)]
years_url = [str(i) for i in range(2000,2019)]
headers = {"Accept-Language": "en-US, en;q=0.5"}

start_time = time()
requests = 0
# For every year in the interval 2000-2018
for year_url in years_url:
    # For every page in the interval 1-4
    for page in pages:
        
        # Make a get request
        response = get('http://www.imdb.com/search/title?release_date=' + year_url + 
        '&sort=num_votes,desc&page=' + page, headers = headers)

        # Pause the loop
        sleep(randint(8,15))

        # Monitor the requests
        requests += 1
        elapsed_time = time() - start_time
        print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
        clear_output(wait = True)

        # Throw a warning for non-200 status codes
        if response.status_code != 200:
            warn('Request: {}; Status code: {}'.format(requests, response.status_code))

        # Break the loop if the number of requests is greater than expected
        if requests > 72:
            warn('Number of requests was greater than expected.')  
            break 

        # Parse the content of the request with BeautifulSoup
        page_html = BeautifulSoup(response.text, 'html.parser')

        # Select all the 50 movie containers from a single page
        mv_containers = page_html.find_all('div', class_ = 'lister-item mode-advanced')
        
        for container in mv_containers:

            name = container.h3.a.text
            names.append(name)

            year = container.h3.find('span', class_ = 'lister-item-year text-muted unbold').text
            years.append(year)

            imdb = float(container.strong.text)
            imdb_ratings.append(imdb)

            if container.find('span', class_ = 'metascore favorable') is not None:
                m_score = container.find('span', class_ = 'metascore favorable').text
                metascores.append(int(m_score))
            else:
                m_score = None
                metascores.append(m_score)

            vote = container.find('span', attrs = {'name':'nv'})['data-value']
            votes.append(int(vote))

            genre = container.find('span',class_='genre').text
            genres.append(genre.strip())

movie_ratings = pd.DataFrame({'movie': names,
                              'year': years,
                              'imdb': imdb_ratings,
                              'metascore': metascores,
                              'votes': votes,
                              'genre':genres})
print(movie_ratings.info())
movie_ratings = movie_ratings[['movie', 'year', 'imdb', 'metascore', 'votes', 'genre']]
movie_ratings.head()
print(movie_ratings.head(10))

#clean the scraped data
#movie_ratings['year'].unique()
#movie_ratings.loc[:, 'year'] = movie_ratings['year'].str[-5:-1].astype(int)
#print(movie_ratings['year'].head(3))
movie_ratings.to_csv('movie_ratings.csv')
