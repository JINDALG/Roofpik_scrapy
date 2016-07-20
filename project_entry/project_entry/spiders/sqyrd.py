# from read_json_sqyrd import convert
import traceback
from pprint import pprint
import re
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
from firebase import firebase
import os
from read_json_sqyrd import convert


class squareyards(scrapy.Spider):
    name = "sqyrd"
    allowed_domains = ["squareyards.com"]   # target site
    start_urls = None

    def __init__(self, filename=None):
        with open(os.path.dirname(__file__) + '/../../link.txt','r') as f:
            self.start_urls = [f.read()]
        self.driver = webdriver.Chrome()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        self.driver.close()

    def parse(self, response):
        fire = firebase.FirebaseApplication('https://abcapp-8345a.firebaseio.com/',None)
        print "some"
        time.sleep(2)
        item = {}
        min_price = max_price = price_per_sqft = min_area = max_area = 0
        is_price_fix = True
        name = description =  code = address = city = location =  status = unit_type = property_type  =""
        amenities ={}
        speciality = {}
        wow_factors =  {}
        index = {}
        connection = {}
        self.driver.get(response.url)
        # try:
        #     WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//img[@src]')))
        # except TimeoutException:
        #     return
        resp = TextResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')

        try:
            name = ("".join(resp.xpath('//h1[@itemprop="name"]//text()').extract())).replace('.','')
            name = (re.sub(r'[^\x00-\x7F]', " ", name))
        except:
            pass

        try:
            min_price = "".join(resp.xpath('//span[@class="price-detail-txt"]/span[@itemprop="minPrice"]//text()').extract())
            isLac = 'L' in min_price
            isCrore = 'Cr' in min_price
            min_price = float(min_price.split()[0])
            try:
                if isLac:
                    min_price *= 100000
            except:
                pass
            try:
                if isCrore:
                    min_price *= 10000000
            except:
                pass
            max_price = "".join(resp.xpath('//span[@class="price-detail-txt"]/span[@itemprop="maxPrice"]//text()').extract())
            isLac = 'L' in max_price
            isCrore = 'Cr' in max_price
            max_price = float(max_price.split()[0])
            try:
                if isLac:
                    max_price *= 100000
            except:
                pass
            try:
                if isCrore:
                    max_price *= 10000000
            except:
                pass
        except :
            min_price = max_price = 0
            pass

        try:
            area = "".join(resp.xpath('//div[@class="proje-detais"]/p//text()').extract())
            area_list = []
            for i in area.split():
                try:
                    area_list += [float(i)]
                except:
                    pass
            min_area = float(area_list[0])
            max_area = float(area_list[1])
        except:
            max_area = min_area

        try:
            price_per = ("".join(resp.xpath('//div[@class="price-details"]/div/div/p[2]/text()').extract())).replace('\n',"").replace('\t',"").replace(',',"")
            price_per_sqft = float(re.findall('\d+', price_per)[0])
            if "sqyrd" in price_per:
                price_per_sqft *= 9
        except:
            price_per_sqft = -1.0

        try:
            address = (",".join(resp.xpath('//ul[@itemprop="address"]//*[contains(@itemprop,"address")]//text()').extract())).replace('\n',"").replace('\t',"")
            address = (re.sub(r'[^\x00-\x7F]', " ", address))
            city = address.split(',')[0]
            location = address.split(',')[-1]
            address = " ".join(address.split(','))
        except:
            pass

        try:
            description = " ".join(resp.xpath('//div[@class="aboutTextBox"]/p//text()').extract())
            description = (re.sub(r'[^\x00-\x7F]', " ", description))
        except:
            pass

        try:
            special = resp.xpath('//div[contains(@class,"AmenitiesBoxBorder")]')
            for spec in special:
                try:
                    label = (" ".join(spec.xpath('span//text()').extract()))
                    label = (re.sub(r'[^\x00-\x7F]', " ", label)).encode('utf8')
                    if label == "":
                        try:
                            speciality['other'] += [re.sub(r'[^\x00-\x7F]'," ",("".join(spec.xpath('div//li//span//text()').extract()))).encode('utf8')]
                        except:
                            speciality['other'] = [re.sub(r'[^\x00-\x7F]'," ",("".join(spec.xpath('div//li//span//text()').extract()))).encode('utf8')]
                    else:
                        speciality[label] = re.sub(r'[^\x00-\x7F]'," ",("".join(spec.xpath('div//li//span//text()').extract()))).encode('utf8')
                except:
                    pass
        except:
            pass

        try:
            amenity_category = resp.xpath('//div[@class="amenitiesSliderBox"]/div')
            for category in amenity_category:
                try:
                    category_name = "".join(category.xpath('div/div[1]/div//text()').extract())
                    category_name = re.sub(r'[^\x00-\x7F]', " ",category_name).encode('utf8')
                    amenities[category_name] = {}
                    aminity_list = category.xpath('div//li')
                    for amenity in aminity_list:
                        try:
                            header = ("".join(amenity.xpath('span[2]//text()').extract())).replace("'","").replace('/','OR')
                            header = re.sub(r'[^\x00-\x7F]'," ",header).encode('utf8')
                            availability = "".join(amenity.xpath('span[2]/@class').extract())
                            if "active" in availability:
                                amenities[category_name][header] = 1
                            else:
                                amenities[category_name][header] = 0
                        except:
                            pass
                except:
                    pass
        except:
            pass
        try:
            status = "".join(resp.xpath('//div[@class="progress-main"]//li[2]//text()').extract())
            status =  re.sub(r'[^\x00-\x7F]'," ",status)
        except:
            pass

        try:
            code = (response.url).split('/')[-2]
        except:
            pass

        try:
            project_details = resp.xpath('//div[contains(@class,"proje-detais")]')
            for details in project_details:
                if "Unit" in "".join(details.xpath('p/span/text()').extract()):
                    unit_type = ("".join(details.xpath('p/text()').extract())).replace('\n',"")
                    unit_type = re.sub(r'[^\x00-\x7F]'," ",unit_type)
                if "Property" in "".join(details.xpath('p/span/text()').extract()):
                    property_type = ("".join(details.xpath('p/text()').extract())).replace('\n',"")
                    property_type = re.sub(r'[^\x00-\x7F]', " ",property_type)
        except:
            pass

        try:
            wow_factor = resp.xpath('//div[contains(@class,"wow-Factors-section")]//li')
            for factor in wow_factor:
                value = ("".join(factor.xpath('span//text()').extract())).replace('\n',"")
                key = ("".join(factor.xpath('small//text()').extract())).replace('\n',"").replace('.','').replace('/','-')
                value = (re.sub(r'[^\x00-\x7F]', " ", value)).encode('utf8')
                key = (re.sub(r'[^\x00-\x7F]', " ", key)).encode('utf8')
                wow_factors[key] = value
        except:
            pass

        try:
            connected_road = resp.xpath('//div[contains(@class,"connect-roads")]//li')
            for road in connected_road:
                try:
                    value = ("".join(road.xpath('span[1]//text()').extract())).split('~')
                    dis = float(value[1].split()[0])
                    connection[value[0].encode('utf8')] = dis
                except:
                    pass
        except:
            pass

        try:
            driver_box = resp.xpath('//div[contains(@class,"decisionDriversBox")]/div/div/div')
            for box in driver_box:
                try:
                    head = ("".join(box.xpath('div//div[@class="projectCounter"]//div[@class="heading"]/text()').extract()))
                    head  = re.sub(r'[^\x00-\x7F]'," ",head).encode('utf8')
                    val = ("".join(box.xpath('div//div[@class="projectCounter"]//div[contains(@class,"Box")]/text()').extract()))
                    val = re.sub(r'[^\x00-\x7F]'," ",val).encode('utf8')
                    index[head] = val  
                except:
                    pass     
        except:
            pass

        try:
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
            if item['name'] != "":
                try :
                    item = convert(item)
                    print fire.put('/','temp',item)
                except:
                    print fire.put('/','temp',{})
                    print traceback.print_exc();
            else:
                print fire.put('/','temp',{})
                print response.url
        except:
            print fire.put('/','temp',{})
            print traceback.print_exc()
            print response.url
        return
    def parse_deep_info(self, abs_url, item):
        deep_item = {}
        self.driver.get(abs_url)
        # try:
        #     WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="unitTopTable table-responsive"]//tr[2]/td[2]')))
        # except TimeoutException:
        #     return
        resp = TextResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')

        min_price = max_price = living_area  = bedrooms = bathrooms = kitchens = servent_rooms = carpet_area = built_up_area =  0
        code = name = ""
        balconies = {}
        Room_private_area = {}
        living_common_area = {}
        open_area = {}
        additional_area = {}
        try:
            code = abs_url.split('/')[-2]
        except:
            pass

        try:
            name = ("".join(resp.xpath('//h1[@itemprop="name"]//text()').extract())).split()[:2]
            name = "-".join(name)
        except:
            pass

        try:
            min_price = "".join(resp.xpath('//div[@class="unitTopTable table-responsive"]//tr[2]/td[2]//text()').extract())
            isLac = 'L' in min_price
            isCrore = 'Cr' in min_price
            min_price = float(min_price.split()[0])
            try:
                if isLac:
                    min_price *= 100000
            except:
                pass
            try:
                if isCrore:
                    min_price  *= 10000000
            except:
                pass
        except:
            pass

        try :
            max_price = "".join(resp.xpath('//div[@class="unitTopTable table-responsive"]//tr[2]/td[3]//text()').extract())
            isLac = 'L' in max_price
            isCrore = 'Cr' in max_price
            max_price = float(max_price.split()[0])   
            try :
                if isLac:
                    max_price *= 100000
            except :
                pass
            try :
                if isCrore:
                    max_price  *= 10000000
            except :
                pass
        except:
            pass    

        try :
            more_info = resp.xpath('//div[@class="unit-left-section"]//ul/li')
            for info in more_info:
                value = "".join(info.xpath('span//text()').extract())
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

                        balconies['count'] = int(value.split()[0])
                        balconies['size_in_sqft'] = int((value.split()[2])[1:])
                except :
                    pass
        except:
            pass        

        try :
            more_info = resp.xpath('//div[@class="unit-loder"]//div[@ng-if="!isFragment"]')
            for info in more_info:
                header = "".join(info.xpath('div//p//text()').extract())
                try :
                    if "Carpet" in header:
                        carpet_area = int(("".join(info.xpath('div//small//text()').extract())).split()[0])
                except :
                    pass
                try :
                    if "BuiltUp" in header:
                        built_up_area = int(("".join(info.xpath('div//small//text()').extract())).split()[0])
                except :
                    pass
        except:
            pass

        try :
            private_areas = resp.xpath('//div[contains(@class,"unitdimensionsArea")]/div/div[1]/div[1]//tr')
            for area in private_areas:
                try :
                    length = breadth = area_sqft = 0.0
                    temp = area.xpath('td[@class="ng-binding"]//text()').extract()
                    # pprint(temp)
                    # input()
                    try :
                        length = float(temp[1])
                    except :
                        pass
                    try :
                        breadth = float(temp[2])
                    except :
                        pass
                    try :
                        area_sqft =  float(temp[3].split()[0])
                    except :
                        pass
                    try :
                        Room_private_area[temp[0].split()[0].encode('utf8')] = {'Length':length, 'Breadth':breadth,'Area' : area_sqft}
                    except :
                        pass
                except :
                    pass
        except :
            pass
        try :
            private_areas = resp.xpath('//div[contains(@class,"unitdimensionsArea")]/div/div[1]/div[2]//tr')
            for area in private_areas:
                try :
                    length = breadth = area_sqft = 0.0
                    temp = area.xpath('td[@class="ng-binding"]//text()').extract()
                    # pprint(temp)
                    # input()
                    try :
                        length = float(temp[1])
                    except :
                        pass
                    try :
                        breadth = float(temp[2])
                    except :
                        pass
                    try :
                        area_sqft =  float(temp[3].split()[0])
                    except :
                        pass
                    try :
                        living_common_area[temp[0].split()[0].encode('utf8')] = {'Length':length, 'Breadth':breadth,'Area' : area_sqft}
                    except :
                        pass
                except :
                    pass
        except :
            pass
        try :
            private_areas = resp.xpath('//div[contains(@class,"unitdimensionsArea")]/div/div[2]/div[1]//tr')
            for area in private_areas:
                try:
                    length = breadth = area_sqft = 0.0
                    temp = area.xpath('td[@class="ng-binding"]//text()').extract()
                    # pprint(temp)
                    # input()
                    try:
                        length = float(temp[1])
                    except:
                        pass
                    try:
                        breadth = float(temp[2])
                    except:
                        pass
                    try:
                        area_sqft = float(temp[3].split()[0])
                    except:
                        pass
                    try:
                        open_area[temp[0].split()[0].encode('utf8')] = {'Length':length, 'Breadth':breadth,'Area' : area_sqft}
                    except:
                        pass
                except:
                    pass
        except:
            pass

        try:
            private_areas = resp.xpath('//div[contains(@class,"unitdimensionsArea")]/div/div[2]/div[2]//tr')
            for area in private_areas:
                try:
                    length = breadth = area_sqft = 0.0
                    temp = area.xpath('td[@class="ng-binding"]//text()').extract()
                    # pprint(temp)
                    # input()
                    try:
                        length = float(temp[1])
                    except:
                        pass
                    try:
                        breadth = float(temp[2])
                    except:
                        pass
                    try:
                        area_sqft = float(temp[3].split()[0])
                    except:
                        pass
                    try:
                        additional_area[temp[0].split()[0].encode('utf8')] = {'Length': length, 'Breadth': breadth,'Area' : \
                        area_sqft}
                    except:
                        pass
                except:
                    pass
        except:
            pass

        deep_item['min_price'] = min_price
        deep_item['max_price'] = max_price
        deep_item['carpet_area'] = carpet_area
        deep_item['built_up_area'] = built_up_area
        deep_item['bedrooms'] = bedrooms
        deep_item['bathrooms'] = bathrooms
        deep_item['balconies'] = balconies
        deep_item['servent_room'] = servent_rooms
        deep_item['living_area'] = living_area
        deep_item['kitchen'] = kitchens
        deep_item['code'] = code.encode('utf8')
        deep_item['room_private_areas'] = Room_private_area
        deep_item['living_common_areas'] = living_common_area
        deep_item['open_areas'] = open_area
        deep_item['additional_areas'] = additional_area

        try :
            item[name.encode('utf8')] += [deep_item]
        except:
            item[name.encode('utf8')] = [deep_item]
