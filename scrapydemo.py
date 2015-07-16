import scrapy

class EPSpeakerSpider(scrapy.Spider):
    name = 'epspeakers'
    start_urls = ['https://ep2015.europython.eu/en/speakers/']
    
    def parse(self, response):
        for url in response.xpath('//li/a[contains(@href, "/conference/")]/@href').extract(): 
            full_url = response.urljoin(url)
            yield scrapy.Request(full_url, callback=self.parse_speakerdetails)
    
    def parse_speakerdetails(self, response):
        item = {}
        item['url'] = response.url
        item['name'] = response.xpath('//section[@class="profile-name"]//h1/text()').extract()[0].strip()
        item['avatar'] = response.urljoin(response.xpath('//img[@class="avatar"]/@src').extract()[0])

        # Getting all attributes about the Speaker
        for field in response.xpath('//dl[@class="dl-horizontal"]//dt'):
            name = field.xpath('.//text()').extract()[0].strip()
            description = ''.join(field.xpath('.//following-sibling::dd[1]//text()').extract()).strip()
            item[name] = description

        # Extracting list of talks
        talks = []
        for talk in response.xpath('//div[@class="speaker-talks well"]//li'):
            talk_title = talk.xpath('.//text()').extract()[0]
            talk_url = response.urljoin(talk.xpath('.//a/@href').extract()[0])
            talks.append({'title': talk_title, 'url': talk_url})
        item['talks'] = talks
        return item
