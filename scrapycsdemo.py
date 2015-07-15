from scrapy.spiders import CrawlSpider

class EPSpeakerSpider(CrawlSpider):
	name = 'epspeakers_crawlspider'
	start_urls = ['https://ep2015.europython.eu/en/speakers/']
	rules = [Rule(LinkExtractor(allow=('/conference/',), callback='parse_speakerdetails'))]

	def parse_speakerdetails(self, response):
		return []

