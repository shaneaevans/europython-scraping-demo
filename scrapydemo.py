import scrapy

class EPSpeakerSpider(scrapy.Spider):
	name = 'epspeakers'
	start_urls = ['https://ep2015.europython.eu/en/speakers/']

	def parse(self, response):
		for url in response.xpath('//li/a[contains(@href, "/conference/")]/@href').extract():
			full_url = response.urljoin(url)
			yield Request(full_url, callback=self.parse_speakerdetails)

	def parse_speakerdetails(self, response):
		return []
