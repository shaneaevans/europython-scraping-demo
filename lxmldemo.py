import urllib
import lxml.html
import lxml.html.soupparser


def print_speakers(root):
    print 'Root:', root

    e = root.xpath('//h3[contains(.,"E")]')
    if e:
        e0 = e[0]
        print 'Heading:', e0

        speakers = e0.xpath('following-sibling::ul[1]/li')
        print 'Speakers:', speakers

        for speaker in speakers:
            print speaker.xpath('.//text()')

url = 'https://ep2015.europython.eu/en/speakers/'

print
print 'Use fast lxml.html library'

reader = urllib.urlopen(url)
tree = lxml.html.parse(reader)
print 'Tree:', tree
root = tree.getroot()
print_speakers(root)


print
print 'soupparser module was added in lxml 2.0.3'

reader = urllib.urlopen(url)
content = reader.read()
root = lxml.html.soupparser.fromstring(content)
print_speakers(root)
