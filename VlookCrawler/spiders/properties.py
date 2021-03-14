import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import os
import re
from scrapy.exceptions import CloseSpider
import pytz
from datetime import datetime
from .config import firstpage, lastpage, firstpage_num, lastpage_num


def getLinksToCrawl():
    allLinks = []
    with open("links.txt","r") as f:
        for line in f:
            allLinks.append(line.strip().split("|")[1])
    
    crawledLinks = []
    with open("data.txt","r") as f:
        for line in f:
            crawledLinks.append(line.strip().split("|")[0])
    print(list(set(allLinks) - set(crawledLinks)))
    return list(set(allLinks) - set(crawledLinks))

def getAllLinks():
    allLinks = []
    with open("links.txt","r") as f:
        for line in f:
            allLinks.append(line.strip().split("|")[1])
    return allLinks

if __name__ == "__main__":
    print(getLinksToCrawl())
    print(len(getLinksToCrawl()))

class VlookCrawler(CrawlSpider):
    name = 'all'
    # start_urls = ['https://vlook.vn/property-location/cho-thue-van-phong-quan-1/']
    start_urls = getLinksToCrawl()
    rules = (
        Rule(LinkExtractor(
            restrict_xpaths='//a[@class = "next page-numbers"]'), callback='loggingPage', follow=True, errback='logError'),
        Rule(LinkExtractor(
                 restrict_xpaths="//div[@class = 'property-item primary-tooltips']/a"),
        callback='parse_item', errback='logError'),)
        
    def loggingPage(self, response):
        seperate = "|"
        if response.url.find("/page/end") != -1:
            with open(f"log_{firstpage_num}_{lastpage_num}.txt", "a+") as f:
                f.write("done")
                f.write("\n")
            raise CloseSpider("achieved limit page")
        formattime = "%Y:%m:%d %H:%M:%S"
        timezone = 'Asia/Saigon'
        str_currenttime = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(pytz.timezone(timezone)).strftime(formattime)
        
        with open(f"log_{firstpage_num}_{lastpage_num}.txt", "a+") as f:
            f.write(str_currenttime)
            f.write(seperate)
            f.write(response.url)
            f.write(seperate)
            f.write("\n")

    def logError(self, failure):
        formattime = "%Y:%m:%d %H:%M:%S"
        timezone = 'Asia/Saigon'
        str_currenttime = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(pytz.timezone(timezone)).strftime(formattime)
        with open("log_err.txt", "a+") as f:
            f.write(str_currenttime)
            f.write("|")
            f.write(str(failure.value.response.status))
            f.write("|")
            f.write(failure.value.response.url)
            f.write("\n")

    def parse_item(self, response):
        xpath_DonGia = "//div[@class = 'price-nhat']/text()"
        xpath_NgayCapNhat = "//p[@class = 'cap-nhat-gia-single']/b/text()"
        xpath_infos = "//li[@class = 'col-sm-12']"
        seperate = "|"
        url = response.url
        DonGia = response.xpath(xpath_DonGia).extract_first()
        if DonGia is None:
            DonGia = "None"
        NgayCapNhat = response.xpath(xpath_NgayCapNhat).extract_first()
        if NgayCapNhat is None:
            NgayCapNhat = "None"

        dict_init_values = {
            "tên tòa nhà" : "None",
            "địa chỉ" : "None",
            "số tầng" : "None",
            "diện tích cho thuê" : "None",
            "giá thuê" : "None",
            "phí quản lý" : "None",
            "phí gửi xe máy" : "None",
            "phí gửi ô tô" : "None",
            "tiền điện" : "None",
            "phí ngoài giờ" : "None",
            "thời gian thiết kế văn phòng" : "None",
            "thời gian thuê" : "None",
            "đặt cọc" : "None",
            "thanh toán" : "None",
        }

        infos = response.xpath(xpath_infos)
        for i in range(1,len(infos) + 1):
            xpath_text = f"//li[@class = 'col-sm-12'][{i}]//text()"
            lst_text = response.xpath(xpath_text).extract()
            info_name = lst_text[0].lower().replace(":","").strip()
            str_value = ""    
            for value in lst_text[1:]:
                str_value = str_value + value + " "
            dict_init_values[info_name] = str_value.strip()
            
        with open("data.txt","a+") as f:
            f.write(url.replace("|","/"))
            f.write(seperate)

            f.write(DonGia)
            f.write(seperate)

            f.write(NgayCapNhat)
            f.write(seperate)

            f.write(dict_init_values["tên tòa nhà"].replace("|","/"))
            f.write(seperate)

            f.write(dict_init_values["địa chỉ"].replace("|","/"))
            f.write(seperate)

            f.write(dict_init_values["số tầng"].replace("|","/"))
            f.write(seperate)
            
            f.write(dict_init_values["diện tích cho thuê"].replace("|","/"))
            f.write(seperate)

            f.write(dict_init_values["giá thuê"].replace("|","/"))
            f.write(seperate)

            f.write(dict_init_values["phí quản lý"].replace("|","/"))
            f.write(seperate)

            f.write(dict_init_values["phí gửi xe máy"].replace("|","/"))
            f.write(seperate)

            f.write(dict_init_values["phí gửi ô tô"].replace("|","/"))
            f.write(seperate)

            f.write(dict_init_values["tiền điện"].replace("|","/"))
            f.write(seperate)

            f.write(dict_init_values["phí ngoài giờ"].replace("|","/"))
            f.write(seperate)

            f.write(dict_init_values["thời gian thiết kế văn phòng"].replace("|","/"))
            f.write(seperate)

            f.write(dict_init_values["thời gian thuê"].replace("|","/"))
            f.write(seperate)

            f.write(dict_init_values["đặt cọc"].replace("|","/"))
            f.write(seperate)

            f.write(dict_init_values["thanh toán"].replace("|","/"))
            f.write("\n")



class SpecificLinks(scrapy.Spider):
    name = 'specific'
    start_urls = ['https://vlook.vn/van-phong-cho-thue/cao-oc-hung-phat-le-van-luong-huyen-nha-be/',
 'https://vlook.vn/van-phong-cho-thue/cmr-building-le-van-luong-huyen-nha-be/',
 'https://vlook.vn/van-phong-cho-thue/hkl-building-nguyen-huu-tho-huyen-nha-be/',
 'https://vlook.vn/van-phong-cho-thue/phu-hoang-anh-building-cho-thue-van-phong-quan-7/',
 'https://vlook.vn/van-phong-cho-thue/pv-gas-tower-nguyen-huu-tho-huyen-nha-be/',
 'https://vlook.vn/van-phong-cho-thue/vinamilk-tower-cho-thue-van-phong-quan-7/']
        
    def parse(self, response):
        xpath_DonGia = "//div[@class = 'price-nhat']/text()"
        xpath_NgayCapNhat = "//p[@class = 'cap-nhat-gia-single']/b/text()"
        xpath_infos = "//li[@class = 'col-sm-12']"
        seperate = "|"
        url = response.url
        DonGia = response.xpath(xpath_DonGia).extract_first()
        if DonGia is None:
            DonGia = "None"
        NgayCapNhat = response.xpath(xpath_NgayCapNhat).extract_first()
        if NgayCapNhat is None:
            NgayCapNhat = "None"

        dict_init_values = {
            "tên tòa nhà" : "None",
            "địa chỉ" : "None",
            "số tầng" : "None",
            "diện tích cho thuê" : "None",
            "giá thuê" : "None",
            "phí quản lý" : "None",
            "phí gửi xe máy" : "None",
            "phí gửi ô tô" : "None",
            "tiền điện" : "None",
            "phí ngoài giờ" : "None",
            "thời gian thiết kế văn phòng" : "None",
            "thời gian thuê" : "None",
            "đặt cọc" : "None",
            "thanh toán" : "None",
        }

        infos = response.xpath(xpath_infos)
        for i in range(1,len(infos) + 1):
            xpath_text = f"//li[@class = 'col-sm-12'][{i}]//text()"
            lst_text = response.xpath(xpath_text).extract()
            info_name = lst_text[0].lower().replace(":","").strip()
            str_value = ""    
            for value in lst_text[1:]:
                str_value = str_value + value + " "
            dict_init_values[info_name] = str_value.strip()
            
        with open("data.txt","a+") as f:
            f.write(url.replace("|","/"))
            f.write(seperate)

            f.write(DonGia)
            f.write(seperate)

            f.write(NgayCapNhat)
            f.write(seperate)

            f.write(dict_init_values["tên tòa nhà"].replace("|","/"))
            f.write(seperate)

            f.write(dict_init_values["địa chỉ"].replace("|","/"))
            f.write(seperate)

            f.write(dict_init_values["số tầng"].replace("|","/"))
            f.write(seperate)
            
            f.write(dict_init_values["diện tích cho thuê"].replace("|","/"))
            f.write(seperate)

            f.write(dict_init_values["giá thuê"].replace("|","/"))
            f.write(seperate)

            f.write(dict_init_values["phí quản lý"].replace("|","/"))
            f.write(seperate)

            f.write(dict_init_values["phí gửi xe máy"].replace("|","/"))
            f.write(seperate)

            f.write(dict_init_values["phí gửi ô tô"].replace("|","/"))
            f.write(seperate)

            f.write(dict_init_values["tiền điện"].replace("|","/"))
            f.write(seperate)

            f.write(dict_init_values["phí ngoài giờ"].replace("|","/"))
            f.write(seperate)

            f.write(dict_init_values["thời gian thiết kế văn phòng"].replace("|","/"))
            f.write(seperate)

            f.write(dict_init_values["thời gian thuê"].replace("|","/"))
            f.write(seperate)

            f.write(dict_init_values["đặt cọc"].replace("|","/"))
            f.write(seperate)

            f.write(dict_init_values["thanh toán"].replace("|","/"))
            f.write("\n")