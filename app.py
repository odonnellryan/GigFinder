import flask
import requests
from urllib import parse
from bs4 import BeautifulSoup
from db import database, Gigs

locations = ['newjersey']

#database.create_table(Gigs)

def get_craigslist_post_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    post_content = soup.find('section', {'id': 'postingbody'})
    return post_content.text if post_content else None


def build_craigslist_data_object(soup, url, location):
    rows = soup.find('div', class_='content').find('span', class_='rows').find_all('p')
    data = []
    for row in rows:
        town = row.find('span', class_='pnr').find('small')
        _location = " ".join([location, town.text.strip()]) if town else location
        post_url = parse.urljoin(url, row.a['href'])
        data.append({
            'website_supplied_id': row['data-pid'],
            'name': row.find('a', class_='hdrlnk').text.strip(),
            'url': post_url,
            'location': _location,
            'datetime': row.find('time')['datetime'],
            'details': get_craigslist_post_details(post_url)
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
                               location=item['location'], datetime=item['datetime'], details=item['details'])


print(insert_into_db(craigslist_searcher(locations)))