import flask
import requests
from urllib import parse
from bs4 import BeautifulSoup
from db import database, Gigs

locations = ['newjersey']

def build_craigslist_data_object(soup, url, location):
    rows = soup.find('div', class_='content').find('span', class_='rows').find_all('p')
    data = []
    for row in rows:
        town = row.find('span', class_='pnr').find('small')
        _location = " ".join([location, town.text.strip()]) if town else location
        data.append({
            'website_supplied_id': row['data-pid'],
            'name': row.find('a', class_='hdrlnk').text.strip(),
            'url': parse.urljoin(url, row.a['href']),
            'location': _location,
            'datetime': row.find('time')['datetime']
        })
    return data

def craigslist_searcher(locations):
    data = []
    for location in locations:
        url = "https://{}.craigslist.org/search/cpg/".format(location)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        data.extend(build_craigslist_data_object(soup, url, location))
    return data

def insert_into_db(data):
    with database.atomic():
        for item in data:
            Gigs.create_or_get(website_supplied_id=item['website_supplied_id'], name=item['name'], url=item['url'],
                               location=item['location'], datetime=item['datetime'])


print(insert_into_db(craigslist_searcher(locations)))