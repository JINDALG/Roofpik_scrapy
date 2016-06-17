from buy.items import BuyItem
import start_url
from pprint import pprint
import re

class acres99Spider(scrapy.Spider):
    page = 1
    name = "mbricks"
    allowed_domains = ["magicbricks.com"]   # target site
    #start_urls = start()
    #start_urls =["http://www.99acres.com/search/property/rent/residential-all/delhi-ncr-all?search_type=QS&search_location=CP1&lstAcn=CP_R&lstAcnId=1&src=CLUSTER&preference=R&selected_tab=4&city=1&res_com=R&property_type=R&isvoicesearch=N&keyword_suggest=delhi%20%2F%20ncr%20(all)%3B&class=A%2CO%2CB&fullSelectedSuggestions=delhi%20%2F%20ncr%20(all)&strEntityMap=W3sidHlwZSI6ImNpdHkifSx7IjEiOlsiZGVsaGkgLyBuY3IgKGFsbCkiLCJDSVRZXzEsIFBSRUZFUkVOQ0VfUiwgUkVTQ09NX1IiXX1d&texttypedtillsuggestion=Delhi&refine_results=Y&Refine_Localities=Refine%20Localities&action=%2Fdo%2Fquicksearch%2Fsearch&suggestion=CITY_1%2C%20PREFERENCE_R%2C%20RESCOM_R&searchform=1&price_max=null'"]
    
    def start_requests(self):
        urls = start_url.start_magic()
        for url in urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        urls = response.xpath('//div[@class="srpAnchor"]/p/a/@href').extract() 
        #urls=['http://www.magicbricks.com/propertyDetails/4-BHK-4000-Sq-ft-Multistorey-Apartment-FOR-Rent-DLF-City-Phase-5-in-Gurgaon&id=4d423230333033343631?from=search']
        if len(urls) == 0:
            return
        for url in urls:
            abs_url = 'http://www.magicbricks.com/' + url
            yield scrapy.Request(abs_url, callback=self.parse_property_info)

        self.page +=1  
        next_url = (response.url).split('/')
        next_url[-1] = "Page-" + str(self.page)
        next_url = '/'.join(next_url) # url of next page
        yield scrapy.Request(next_url, callback=self.parse)

    def parse_property_info(self, response):    

        item = BuyItem()

        price = price_per_sqft  = min_area = max_area = bathrooms = bedrooms = SuperBuiltupArea = is_resale =  0
        is_price_fix = 1
        address = city = location = age_of_property = agent_name = agent_type = launch_date = status = amenities = ""
        speciality  = {}
        more_info = []

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
        item['possession_status'] = status.encode('utf8')
        item['agent_name'] = agent_name.encode('utf8')
        item['agent_type'] = agent_type.encode('utf8')
        item['amenities'] = amenities.encode('utf8')
        item['speciality'] = speciality
        item['more_info'] = more_info
        item['is_resale'] = is_resale
        item['url'] = response.url




