from squareyard.items import SquareyardItem
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
        item = SquareyardItem()

        min_price = max_price = price_per_sqft  = min_area = max_area  =  0
        is_price_fix = 1
        name = description =  code = address = city = location =  status = unit_type = property_type  =""
        amenities ={}
        speciality = {}
        wow_factors =  {}
        index = {}
        connection = []
        self.driver.get(response.url)
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//img[@src]')))
        except TimeoutException:
            return
        resp = TextResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')

        try :
            name = ''.join(resp.xpath('//h1[@itemprop="name"]//text()').extract())
        except :
            pass

        try :
            full_price = ''.join(resp.xpath('//span[@class="price-detail-txt"]//text()').extract())
            full_price_list = []
            for i in full_price.split() :
                try :
                    full_price_list += [float(i)]
                except :
                    pass
            min_price = float(full_price_list[0])
            try :
                max_price = float(full_price_list[1])
            except :
                pass
            try :
                if "Lac" in full_price:
                    min_price *= 100000
                    max_price *= 100000
            except :
                pass
            try :
                if "Cr" in full_price:
                    min_price  *= 10000000
                    max_price  *= 10000000
            except :
                pass
        except :
            pass

        try :
            area = ''.join(resp.xpath('//div[@class="proje-detais"]/p//text()').extract())
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
        
        try:
            description = '\n'.join(resp.xpath('//div[@class="aboutTextBox"]/p//text()').extract())
        except:
            pass

        try :
            special = resp.xpath('//div[contains(@class,"AmenitiesBoxBorder")]')
            speciality['other'] = []
            for spec in special:
                try :
                    label = (''.join(spec.xpath('span//text()').extract())).encode('utf8')
                    if label == "":
                        speciality['other'] += [(''.join(spec.xpath('div//li//span//text()').extract())).encode('utf8')]
                    else :
                        speciality[label] = (''.join(spec.xpath('div//li//span//text()').extract())).encode('utf8')
                except :
                    pass
        except :
            pass

        try :
            amenity_category = resp.xpath('//div[@class="amenitiesSliderBox"]/div')
            for category in amenity_category:
                try :
                    category_name = ''.join(category.xpath('div/div[1]/div//text()').extract()).encode('utf8')
                    amenities[category_name] = {}
                    aminity_list = category.xpath('div//li')
                    for amenity in aminity_list:
                        try :
                            header = (''.join(amenity.xpath('span[2]//text()').extract())).encode('utf8')
                            availability = ''.join(amenity.xpath('span[2]/@class').extract())
                            if "active" in availability:
                                amenities[category_name][header] = True
                            else :
                                amenities[category_name][header] = False
                        except :
                            pass
                except :
                    pass
        except :
            pass
        try :
            status = ''.join(resp.xpath('//div[@class="progress-main"]//li[2]//text()').extract())
        except :
            pass

        try :
            code = (response.url).split('/')[-2]
        except :
            pass

        try :
            project_details = resp.xpath('//div[contains(@class,"proje-detais")]')
            for details in project_details:
                if "Unit" in ''.join(details.xpath('p/span/text()').extract()):
                    unit_type = (''.join(details.xpath('p/text()').extract())).replace('\n','')
                if "Property" in ''.join(details.xpath('p/span/text()').extract()):
                    property_type = (''.join(details.xpath('p/text()').extract())).replace('\n','')
        except :
            pass

        try :
            wow_factor = resp.xpath('//div[contains(@class,"wow-Factors-section")]//li')
            for factor in wow_factor:
                value = (''.join(factor.xpath('span//text()').extract())).replace('\n','').encode('utf8')
                key = (''.join(factor.xpath('small//text()').extract())).replace('\n','').encode('utf8')
                wow_factors[key] = value
        except :
            pass

        try :
            connected_road = resp.xpath('//div[contains(@class,"connect-roads")]//li')
            for road in connected_road:
                try :
                    value = (''.join(road.xpath('span[1]//text()').extract())).split('~')
                    dis = float(value[1].split()[0])
                    connection += [{'name':value[0].encode('utf8'), 'distance': dis}]
                except :
                    pass
        except :
            pass

        try :
            driver_box = resp.xpath('//div[contains(@class,"decisionDriversBox")]/div/div/div')
            for box in driver_box:
                try :
                    head = (''.join(box.xpath('div//div[@class="projectCounter"]//div[@class="heading"]/text()').extract())).encode('utf8')
                    val = (''.join(box.xpath('div//div[@class="projectCounter"]//div[contains(@class,"Box")]/text()').extract())).encode('utf8')
                    index[head] = val  
                except :
                    pass     
        except :
            pass

        item['name'] = name.encode('utf8')
        item['min_price'] = min_price
        item['max_price'] = max_price
        item['price_per_sqft'] = price_per_sqft
        item['address'] = address.encode('utf8')
        item['city'] = city.encode('utf8')
        item['location'] = location.encode('utf8')
        item['min_area'] = min_area
        item['max_area'] = max_area
        item['possession_status'] = status.encode('utf8')
        item['amenities'] = amenities
        item['speciality'] = speciality
        item['url'] = response.url
        item['code'] = code.encode('utf8')
        item['description'] = description.encode('utf8')
        item['unit_type'] = unit_type.encode('utf8')
        item['property_type'] = property_type.encode('utf8')
        item['index'] = index
        item['connecting_road'] = connection
        item['wow_factors'] = wow_factors
        item['more_info'] = {}

        urls = resp.xpath('//div[@class="bhkDetails"]//a/@href').extract()
        for url in urls:
            abs_url = 'http://www.squareyards.com' + url
            self.parse_deep_info(abs_url, item['more_info'])
        
        yield item
        input()

    def parse_deep_info(self, abs_url, main_item):
        item = {}
        self.driver.get(abs_url)
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@itemprop="minPrice"]')))
        except TimeoutException:
            return
        resp = TextResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')

        balconies =min_price = max_price = living_area  = bedrooms = bathrooms = kitchens = servent_rooms = carpet_area = built_up_area =  0
        code = name = ""
        try :
            code = ((response.url).split('/')[-2]).encode('utf8')
        except :
            pass

        try :
            name = (''.join(resp.xpath('//h1[@itemprop="name"]//text()').extract())).split()
            name = ''.join([name[0],name[1]])
        except :
            pass

        try :
            full_price = ''.join(resp.xpath('//span[@itemprop="minPrice"]//text()').extract())
            min_price = float(full_price.split()[0])   
            try :
                if "Lac" in full_price:
                    min_price *= 100000
            except :
                pass
            try :
                if "Cr" in full_price:
                    min_price  *= 10000000
            except :
                pass
        except:
            pass

        try :
            full_price = ''.join(resp.xpath('//span[@itemprop="maxPrice"]//text()').extract())
            max_price = float(full_price.split()[0])   
            try :
                if "Lac" in full_price:
                    max_price *= 100000
            except :
                pass
            try :
                if "Cr" in full_price:
                    max_price  *= 10000000
            except :
                pass
        except:
            pass    

        try :
            more_info = resp.xpath('//div[@class="unit-left-section"]//ul/li')
            for info in more_info:
                value = ''.join(info.xpath('span//text()').extract())
                try :
                    if "Living" in value:
                        living_area = int(value.split()[0])
                except :
                    pass
                try :
                    if "Bed" in value:
                        bedrooms = int(value.split()[0])
                except:
                    pass
                try :
                    if "Bath" in value:
                        bathrooms = int(value.split()[0])
                except :
                    pass
                try :
                    if "Kitchen" in value:
                        kitchens = int(value.split()[0])
                except :
                    pass
                try :
                    if "Servant" in value:
                        servent_rooms = int(value.split()[0])
                except :
                    pass
                try :
                    if "Balcon" in value:
                        balconies = int(value.split()[0])
                except :
                    pass
        except:
            pass        

        try :
            more_info = resp.xpath('//div[@class="unit-loder"]//div[@ng-if="!isFragment"]')
            for info in more_info:
                header = ''.join(info.xpath('div//p//text()').extract())
                try :
                    if "Carpet" in value:
                        carpet_area = int((''.join(info.xpath('div//small//text()').extract())).split()[0])
                except :
                    pass
                try :
                    if "BuiltUp" in value:
                        built_up_area = int((''.join(info.xpath('div//small//text()').extract())).split()[0])
                except :
                    pass
        except:
            pass

        item['min_price'] = min_price
        item['max_price'] = max_price
        item['carpet_area'] = carpet_area
        item['built_up_area'] = built_up_area
        item['bedrooms'] = bedrooms
        item['bathrooms'] = bathrooms
        item['balconies'] = balconies
        item['servent_room'] = servent_rooms
        item['living_area'] = living_area
        item['kitchen'] = kitchens
        item['code'] = code.encode('utf8')

        if name in main_item:
            main_item[name] += [item]
        else :
            main_item[name] = [item]