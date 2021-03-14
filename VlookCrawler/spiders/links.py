from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import os
import re
from scrapy.exceptions import CloseSpider
import pytz
from datetime import datetime
from .config import firstpage, lastpage, firstpage_num, lastpage_num

class LinksCrawler(CrawlSpider):
    name = 'links'
    start_urls = ['https://vlook.vn/property-location/cho-thue-van-phong-quan-7/']
    rules = (
        Rule(LinkExtractor(
            restrict_xpaths='//a[@class = "next page-numbers"]'), callback='parse_item', follow=True, errback='logError')
            ,)
    def parse_item(self, response):
        xpath_links = "//div[@class = 'property-item primary-tooltips']/a/@href"
        links = response.xpath(xpath_links).extract()
        with open("linksQuan7.txt","a+") as f:
            for link in links:
                f.write(response.url)
                f.write("|")
                f.write(link)
                f.write("\n")
