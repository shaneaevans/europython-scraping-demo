import requests
import time

from BeautifulSoup import BeautifulSoup


BASE_URL = 'https://ep2015.europython.eu'
MAX_RETRIES = 5


def get_request(url, retried=0):
    # Exception handling
    try:
        # Doing synchronous request, blocking every time we do a new request.
        return requests.get(BASE_URL + url)
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectTimeout,
            requests.exceptions.ConnectionError) as e:
        if retried < MAX_RETRIES:
            retried += 1
            print "Got %s. Waiting 5 seconds and retrying for the %s time..." % (e.message, retried)
            time.sleep(5)
            return get_request(url, retried=retried)
        else:
            print "Got %s. Giving up" % e.message
            return


def get_speaker(url):

    response = get_request(BASE_URL + url)
    if not response:
        return
    soup = BeautifulSoup(response.content)
    item = {}
    item['name'] = soup.find('section', attrs={'class': 'profile-name'}).h1.text
    item['avatar'] = BASE_URL + soup.find('img', attrs={'class': 'avatar'})['src']
    item['url'] = url
    item['talks'] = []
    for talk in soup.find('div', attrs={'class': 'speaker-talks well'}).dl.dd.ul.li:
        item['talks'].append({'name': talk.text, 'url': BASE_URL + talk['href']})
    for dl in soup.findAll('dl', attrs={'class': 'dl-horizontal'}):
        for dt in dl.findChildren('dt'):
            name = dt.text
            value = dt.findNext('dd').text
            item[name] = value
    return item


# Speakers url is https://ep2015.europython.eu/en/speakers/
resp = get_request('/en/speakers/')

if resp:
    # Let's parse the received html
    soup = BeautifulSoup(resp.content)

    # All the links are in a div with class=cms
    conference_container = soup.find('div', attrs={'class': 'cms'})

    # Inside that div, the ponent links are inside li tags
    speaker_links = conference_container.findAll('li')

    for speaker_link in speaker_links:
        print get_speaker(speaker_link.a['href'])
