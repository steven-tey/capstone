"""Scrape startups-list.com."""

import urllib.request
import pandas as pd
from bs4 import BeautifulSoup


BASE_URL = 'http://www.startups-list.com/'
URL = 'http://www.startups-list.com/'
r = urllib.request.urlopen(URL).read()
soup = BeautifulSoup(r, 'lxml')

cities = soup.findAll('a')
cities = cities[:30]
start_up_names = []
city_names = []
descriptions = []
headlines = []
for city in cities:
    city_url = city['href']
    city_name = city.h3.text.replace('\n', '')[2:-2]
    print(city_name)
    city_page = BeautifulSoup(urllib.request.urlopen(city_url).read(), 'lxml')
    names = city_page.findAll('h1')[2:-2]
    descs = city_page.findAll('p')[1:-1]
    start_up_names.extend([name.text[13:-25] for name in names])
    headlines.extend([desc.strong.text[3:] for desc in descs])
    descriptions.extend([desc.text.split("\n\n")[-1][11:] for desc in descs])

data = {'name': start_up_names,
        'tagline': headlines,
        'description': descriptions}

startups_df = pd.DataFrame(data)
startups_df = startups_df.reindex(columns=['name', 'tagline', 'description'])
startups_df.to_csv('startups.csv', index=False)
