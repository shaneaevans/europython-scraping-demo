import requests
from BeautifulSoup import BeautifulSoup

base_url = 'https://ep2015.europython.eu'

# Speakers url is https://ep2015.europython.eu/en/speakers/
resp = requests.get('{}/en/speakers/'.format(base_url))

# Let's parse the received html
soup = BeautifulSoup(resp.content)

# All the links are in a div with class=cms
conference_container = soup.find('div', attrs={'class': 'cms'})

# Inside that div, the ponent links are inside li tags
speaker_links = conference_container.findAll('li')

for speaker_link in speaker_links:
    print speaker_link.text, '{}{}'.format(base_url, speaker_link.a['href'])
