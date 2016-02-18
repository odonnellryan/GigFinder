import requests
from requests_futures.sessions import FuturesSession
from urllib import parse
from bs4 import BeautifulSoup
import settings
import urllib
import db
from db import Gigs
from datetime import datetime, timedelta

CRAIGSLIST_SITE = 'sof'

def get_craigslist_post_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    post_content = soup.find('section', {'id': 'postingbody'})
    return post_content.text if post_content else None


def build_craigslist_data_object(soup, url, location, category):
    rows = soup.find('div', class_='content').find('span', class_='rows').find_all('p')
    data = []
    for row in rows:
        town = row.find('span', class_='pnr').find('small')
        _location = " ".join([location, town.text.strip()]) if town else location
        post_url = parse.urljoin(url, row.a['href'])
        data.append({
            'website': 'craigslist',
            'category': category,
            'website_supplied_id': row['data-pid'],
            'name': row.find('a', class_='hdrlnk').text.strip(),
            'url': post_url,
            'location': _location,
            'datetime': row.find('time')['datetime'],
            'details': get_craigslist_post_details(post_url) if settings.GET_CRAIGSLIST_POST_DETAILS else None
        })
    return data


def craigslist_searcher(locations, site=None):
    for location in locations:
        url = "https://{}.craigslist.org/search/{}/".format(location, (site or CRAIGSLIST_SITE))
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        db.insert_into_db(build_craigslist_data_object(soup, url, location, 'gigs, computer'))


def get_craigslist_cities():
    locations = {}
    cities_page = "https://www.craigslist.org/about/sites"
    response = requests.get(cities_page)
    soup = BeautifulSoup(response.content, 'lxml')
    countries = soup.find_all('h1')
    location_containers = soup.find_all('div', class_='colmask')
    for index, location in enumerate(location_containers):
        cities = [urllib.parse.urlparse(a['href']).hostname.split('.')[0] for a in location.find_all('a')]
        locations[countries[index].text] = cities
    return locations


def insert_callback(session, response):
    soup = BeautifulSoup(response.content, 'lxml')
    location = urllib.parse.urlparse(response.url).hostname.split('.')[0]
    print("Executing callback for:" + location)
    data = build_craigslist_data_object(soup, response.url, location, 'gigs, computer')
    db.insert_into_db(data)



def async_requests(locations, site=None):
    session = FuturesSession()
    check_date = datetime.now() + timedelta(hours=-4)
    for location in locations:
        gig = Gigs.select().where(Gigs.location.contains(location)).order_by(Gigs.datetime.desc()).first()
        if (gig is None) or ((datetime.strptime(gig.datetime, '%Y-%m-%d %H:%M') < check_date)):
            url = "https://{}.craigslist.org/search/{}/".format(location, (site or CRAIGSLIST_SITE))
            future = session.get(url, background_callback=insert_callback)