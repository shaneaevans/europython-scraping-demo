import requests
import time

from BeautifulSoup import BeautifulSoup


class BSCrawler(object):
    base_url = 'https://ep2015.europython.eu'
    max_retries = 5

    def __init__(self):
        self.session = requests.Session()

    def start_crawl(self):
        # Speakers url is https://ep2015.europython.eu/en/speakers/
        response = self.make_request(self.base_url + '/en/speakers/')
        if response:
            # Let's parse the received html
            soup = BeautifulSoup(response.content)

            # All the links are in a div with class=cms
            conference_container = soup.find('div', attrs={'class': 'cms'})

            # Inside that div, the ponent links are inside li tags
            speaker_links = conference_container.findAll('li')

            for speaker_link in speaker_links:
                print self.get_speaker(speaker_link.a['href'])

    def make_request(self, url, retried=0):
        # Exception handling
        try:
            # Doing synchronous request, blocking every time we do a new request.

            return self.session.get(url)
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectTimeout,
                requests.exceptions.ConnectionError) as e:
            if retried < self.max_retries:
                retried += 1
                print "Got %s. Waiting 5 seconds and retrying for the %s time..." % (e.message, retried)
                time.sleep(5)
                return self.make_request(url, retried=retried)
            else:
                print "Got %s. Giving up" % e.message
                return

    def get_speaker(self, url):
        """ Get speaker details """
        response = self.make_request(self.base_url + url)
        if not response:
            return
        soup = BeautifulSoup(response.content)
        item = {}
        item['name'] = soup.find('section', attrs={'class': 'profile-name'}).h1.text
        item['avatar'] = self.base_url + soup.find('img', attrs={'class': 'avatar'})['src']
        item['url'] = url
        item['talks'] = []
        for talk in soup.find('div', attrs={'class': 'speaker-talks well'}).dl.dd.ul.li:
            item['talks'].append({'name': talk.text, 'url': self.base_url + talk['href']})
        for dl in soup.findAll('dl', attrs={'class': 'dl-horizontal'}):
            for dt in dl.findChildren('dt'):
                name = dt.text
                value = dt.findNext('dd').text
                item[name] = value
        return item


BSCrawler().start_crawl()

