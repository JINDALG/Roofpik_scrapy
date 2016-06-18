from buy.items import BuyItem
import start_url
from pprint import pprint
import re
import month
import scrapy
import time
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy.http import TextResponse
from scrapy import signals
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

class squareyards(scrapy.Spider):
    name = "sqyrd"
    allowed_domains = ["squareyards.com"]   # target site
    #start_urls = start()
    #start_urls =["http://www.99acres.com/search/property/rent/residential-all/delhi-ncr-all?search_type=QS&search_location=CP1&lstAcn=CP_R&lstAcnId=1&src=CLUSTER&preference=R&selected_tab=4&city=1&res_com=R&property_type=R&isvoicesearch=N&keyword_suggest=delhi%20%2F%20ncr%20(all)%3B&class=A%2CO%2CB&fullSelectedSuggestions=delhi%20%2F%20ncr%20(all)&strEntityMap=W3sidHlwZSI6ImNpdHkifSx7IjEiOlsiZGVsaGkgLyBuY3IgKGFsbCkiLCJDSVRZXzEsIFBSRUZFUkVOQ0VfUiwgUkVTQ09NX1IiXX1d&texttypedtillsuggestion=Delhi&refine_results=Y&Refine_Localities=Refine%20Localities&action=%2Fdo%2Fquicksearch%2Fsearch&suggestion=CITY_1%2C%20PREFERENCE_R%2C%20RESCOM_R&searchform=1&price_max=null'"]
    def __init__(self, filename=None):
        self.driver = webdriver.Chrome()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self,spider):
        self.driver.close()

    def start_requests(self):
        urls = start_url.start_sqyrd()
        for url in urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        self.driver.get(response.url)

        while True:
            time.sleep(1)
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//p[@class="propertyName"]/a')))
            except TimeoutException:
                return
            resp = TextResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
            urls = resp.xpath('//p[@class="propertyName"]/a/@href').extract()
            pprint(urls)
            #urls=['http://www.magicbricks.com/propertyDetails/270-Sq-ft-Studio-Apartment-FOR-Sale-Vatika-City-in-Gurgaon&id=4d423230333337333839?from=search']
            if len(urls) == 0:
                return
            for url in urls:
                abs_url = 'http://www.squareyards.com' + url
                yield scrapy.Request(abs_url, callback=self.parse_property_info)

            try :
                link = self.driver.find_element_by_xpath('//ul[@class="newpagination"]/li[2]')
                actions = ActionChains(self.driver)
                actions.click(link)
                actions.perform()
            except:
                return

    def parse_property_info(self, response):
        item = BuyItem()

        price = price_per_sqft  = min_area = max_area = bathrooms = bedrooms = SuperBuiltupArea = is_resale =  0
        is_price_fix = 1
        code = address = city = location = age_of_property = agent_name = agent_type = launch_date = status = amenities = posted_on = ""
        speciality  = {}
        more_info = []
        self.driver.get(response.url)
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@class="price-detail-txt"]')))
        except TimeoutException:
            return
        resp = TextResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')

        try :
            full_price = ''.join(resp.xpath('//span[@class="price-detail-txt"]//text()').extract())
            full_price_list = []
            for i in full_price.split() :
                try :
                    full_price_list += [float(i)]
                except :
                    pass
            price = float(full_price_list[0])
            if "Lac" in full_price:
                price *= 100000
            if "Cr" in full_price:
                price  *= 1000000
        except :
            pass

        try :
            area = ''.join(resp.xpath('////div[@class="proje-detais"]/p//text()').extract())
            area_list = []
            for i in area.split() :
                try :
                    area_list += [float(i)]
                except :
                    pass
            min_area = float(area_list[0])
            max_area = float(area_list[1])
        except :
            max_area = min_area

        try:
            price_per = (''.join(resp.xpath('//div[@class="price-details"]/div/div/p[2]/text()').extract())).replace('\n','').replace('\t','').replace(',','')
            priceunit = price_per
            price_per_sqft = []
            for i in price_per.split() :
                try :
                    price_per_sqft += [float(i)]
                except :
                    pass
            price_per_sqft = int(price_per_sqft[0])
            if "sqyrd" in priceunit:
                price_per_sqft *= 9
            
        except:
            pass

        try :
            address = (','.join(resp.xpath('//ul[@itemprop="address"]//*[contains(@itemprop,"address")]//text()').extract())).replace('\n','').replace('\t','')
            city = address.split(',')[0]
            location = address.split(',')[-1]
            address = ' '.join(address.split(','))
        except:
            pass

        datalist = resp.xpath('//div[@class="bhkDetails"]/div')
        for data in datalist:
            try :
                info = (''.join(data.xpath('div/ul/li[1]//text()').extract()))
                info_list = []
                for i in info.split() :
                    try :
                        info_list += [float(i)]
                    except :
                        pass
                bhk = float(info_list[0])
                size = float(info_list[1])
            except :
                pass

            try :
                info = (''.join(data.xpath('div/ul/li[2]//text()').extract()))
                info_list = []
                for i in info.split() :
                    try :
                        info_list += [float(i)]
                    except :
                        pass
                rate = info_list[0]
                if "Lac" in info:
                    rate *= 100000
                if "Cr" in info:
                    rate  *= 1000000
            except :
                pass

            try :
                more_info += [(bhk,size,rate)]
            except :
                pass
        try:
            description = (''.join(resp.xpath('//div[contains(@class,"aboutTextBox")]/p/p[1]//text()').extract())).replace('\n','')
        except:
            pass

        special = resp.xpath('//div[contains(@class,"AmenitiesBoxBorder")]')
        for spec in special:
            label = ''.join(spec.xpath('span//text()').extract())
            speciality[label] = ''.join(spec.xpath('div//li//span//text()').extract())

        amenities = ','.join(resp.xpath('//div[@class="amenitiesSliderBox"]//li//span[contains(@class," active")]//text()').extract())

        status = ''.join(resp.xpath('//div[@class="progress-main"]//li[2]//text()').extract())

        item['price'] = price
        item['price_per_sqft'] = price_per_sqft
        item['is_price_fix'] = is_price_fix
        item['address'] = address.encode('utf8')
        item['city'] = city.encode('utf8')
        item['location'] = location.encode('utf8')
        item['min_area'] = min_area
        item['max_area'] = max_area
        item['bathrooms'] = bathrooms
        item['bedrooms'] = bedrooms
        item['SuperBuiltupArea'] = SuperBuiltupArea
        item['age_of_property'] = age_of_property.encode('utf8')
        item['launch_date'] = launch_date.encode('utf8')
        item['posted_on']  = posted_on.encode('utf8')
        item['possession_status'] = status.encode('utf8')
        item['agent_name'] = agent_name.encode('utf8')
        item['agent_type'] = agent_type.encode('utf8')
        item['amenities'] = amenities.encode('utf8')
        item['speciality'] = speciality
        item['more_info'] = more_info
        item['is_resale'] = is_resale
        item['url'] = response.url
        item['code'] = code.encode('utf8')
        item['description'] = description.encode('utf8')
        

        yield item
        input()

