import scrapy
from scrapy.crawler import CrawlerProcess
#from hk01Spider.items import Hk01SpiderItem
import subprocess

class Hk01SpiderItem(scrapy.Item):
    name = scrapy.Field()
    tagNumber = scrapy.Field()

class hk01Spider(scrapy.Spider):
    def makeUrlsList():
        list = [f'https://www.hk01.com/tag/{tag}' for tag in range(1,10000)]
        return list
    def makeUrlsGenerator():
        for tag in range(1,10000):
            yield f'https://www.hk01.com/tag/{tag}'

    name = "hk01Spider"
    start_urls = makeUrlsGenerator()

    def parse(self, response):
        item = Hk01SpiderItem()
        item['name'] = response.xpath('//div/h2/text()').extract()[0]
        item['tagNumber'] = response.url.split('/')[4]
        subprocess.run('clear')
        print(f'''{item['tagNumber']}/9999 scraped''')
        #print(item['tagNumber'], item['name'])
        yield item

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'FEED_FORMAT': 'json',
    'FEED_URI': 'tags.json',
    'LOG_LEVEL': 'WARNING'
})
process.crawl(hk01Spider)
process.start()
