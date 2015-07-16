from nltk import sent_tokenize
from nltk.tag.stanford import NERTagger

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class EPSpeakerSpider(CrawlSpider):
    name = 'epspeakers_crawlspider'
    start_urls = ['https://ep2015.europython.eu/en/speakers/']
    rules = [
        Rule(LinkExtractor(allow=('/conference/',)),
             callback='parse_speakers')
    ]
    ner = NERTagger('./NER/classifiers/english.all.3class.distsim.crf.ser.gz',
                    './NER/stanford-ner.jar',
                    encoding='utf-8')

    def parse_speakers(self, response):
        item = {}
        item['url'] = response.url

        bio = response.xpath(
            '//*[text()="Compact biography"]/following-sibling::'
            'dd//text()[normalize-space()]').extract()[0]

        # Speaker name is usually in the first sentence
        bio_first_sentence = sent_tokenize(bio)[:1][0]

        tags = self.ner.tag(bio_first_sentence.split())

        speaker_name = ''
        for tag in tags:
            if tag[1] == 'PERSON':
                speaker_name += '%s ' % tag[0]
        item['name'] = speaker_name.strip()

        return item
