import flask
import requests
from urllib import parse
from bs4 import BeautifulSoup

locations = ['newjersey']

def build_craigslist_data_object(soup, url, location):
    rows = soup.find('div', class_='content').find('span', class_='rows').find_all('p')
    data = {}
    for row in rows:
        town = row.find('span', class_='pnr').find('small')
        _location = " ".join([location, town.text.strip()]) if town else location
        data[row['data-pid']] = {
            'name': row.find('a', class_='hdrlnk').text.strip(),
            'url': parse.urljoin(url, row.a['href']),
            'location': _location
        }
    return data

def craigslist_searcher(locations):
    data = []
    for location in locations:
        url = "https://{}.craigslist.org/search/cpg/".format(location)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        data.append(build_craigslist_data_object(soup, url, location))
    return data

print(craigslist_searcher(locations))