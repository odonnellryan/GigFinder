import requests
from urllib import parse
from bs4 import BeautifulSoup
import settings


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


def craigslist_searcher(locations):
    data = []
    for location in locations:
        url = "https://{}.craigslist.org/search/cpg/".format(location)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        data.extend(build_craigslist_data_object(soup, url, location, 'gigs, computer'))
    return data
