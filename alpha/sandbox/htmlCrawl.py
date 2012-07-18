
import sys
sys.path.append(r'\\data\homes1$\jhkoivis\Downloads')

import scrapy
from scrapy.contrib.spiders import CrawlSpider #,Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from tutorial.items import DmozItem
from urlparse import urlparse

class DmozSpider(CrawlSpider):
    name = "dmoz"
    allowed_domains = ["example.com"]
    start_urls = ["www.example.com/page-1",        #name of website
                  "www.example.com/page-2",
                  "www.example.com/page-3"]                                              #pages to be crawled
    
def parse(self, response):
    hxs=HtmlXPathSelector(response)
    data = hxs.select('//div[@class="inner"]')
    items = []
    for test in data:
        item = DmozItem()
        item['name']=test.select('div[@class="com"]/span[@class="title"]/a/text()').extract() 
        item['link']=test.select('div[@class="com"]/span[@class="title"]/a/@href').extract() 
        item['address']=test.select('div[@class="con"]//div[@class="Desc"]/text()').extract()
        item['phoneno']=test.select('div[@class="con"]/div[@class="Desc"]/p/span/text()').extract()
        items.append(item)
    return items

print parse()