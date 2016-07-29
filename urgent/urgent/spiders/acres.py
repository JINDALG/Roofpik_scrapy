#!usr/bin/python -tt
import scrapy 
from pprint import pprint
import re
import os
import json
class acres99Spider(scrapy.Spider):
    name = "99acres"
    obj = None
    allowed_domains = ["99acres.com"]   # target site
    #start_urls = start()
    # start_urls = ['http://www.99acres.com/search/property/rent/residential-all/vipul-greens-sector-48-gurgaon?search_type=QS&search_location=CP1&lstAcn=CP_R&lstAcnId=1&src=CLUSTER&preference=R&selected_tab=4&city=8&res_com=R&property_type=R&type_rescom=none&isvoicesearch=N&keyword_suggest=vipul%20greens%2C%20sector-48%20gurgaon%3B&fullSelectedSuggestions=vipul%20greens%2C%20sector-48%20gurgaon&strEntityMap=W3sidHlwZSI6InByb2plY3QifSx7IjEiOlsidmlwdWwgZ3JlZW5zLCBzZWN0b3ItNDggZ3VyZ2FvbiIsIlBST0pFQ1RfNjY4LCBDSVRZXzgsIExPQ0FMSVRZXzI0NjgsIFBSRUZFUkVOQ0VfUiwgUkVTQ09NX1IiXX1d&texttypedtillsuggestion=vipul&building_id=668%2C668&refine_results=Y&Refine_Localities=Refine%20Localities&action=%2Fdo%2Fquicksearch%2Fsearch&suggestion=PROJECT_668%2C%20CITY_8%2C%20LOCALITY_2468%2C%20PREFERENCE_R%2C%20RESCOM_R&searchform=1&price_min=null&price_max=null']    
    start_urls = ['http://www.99acres.com/rent-property-in-sector-81-gurgaon-ffid-page-3?Building_id=11892&noxid=Y']    
    def __init__(self, filename=None):
        with open(os.path.dirname(__file__) + '/../../link.txt','r') as f:
            self.start_urls = [f.read()]
        self.obj = {}

    def parse(self, response):
        try :
            urls = response.xpath('//div[@class="wrapttl"]/div/a/@href').extract() 
            new_lst = response.xpath('//div[@class="wrapttl"]//text()').extract()   

            if len(urls) == 0:
                return
            project = response.xpath('//div[@title="View property details"]')
            for entry in project:
                try :
                    price = ''.join(entry.xpath('div[@class="wrapttl"]//b[contains(@id,"rs")]//text()').extract())
                    price = price.encode('utf8')
                    print price,"\n\n\n\n"
                    iscr = 'Crore' in price
                    islac = 'Lac' in price
                    price = float(price.replace(',','').split()[0])
                    if islac:
                        price *= 100000
                    if iscr:
                        price *= 10000000
                    price = int(price)
                    bhk = ''.join(entry.xpath('div[@class="wrapttl"]/div[1]/a//text()').extract())
                    bhk = bhk.split(',')[0].replace('.5','')
                    if "bhk" in bhk or "BHK" in bhk:
                        ppf = ''.join(entry.xpath('div[@class="srpDetail"]//div[@class="srpDataWrap"]/span[1]/b[1]//text()').extract())
                        ppf = float(ppf.split()[0])
                        ppf = price/ppf
                        if bhk in self.obj:
                            self.obj[bhk]['min'] = self.obj[bhk]['min'] if price > self.obj[bhk]['min'] else price
                            self.obj[bhk]['max'] = self.obj[bhk]['max'] if price < self.obj[bhk]['max'] else price
                            self.obj[bhk]['count'] += 1
                            self.obj[bhk]['avg'] += ppf
                        else :
                            self.obj[bhk] = {'min':price, 'max':price, 'count':1,'avg':ppf}
                except :
                    pass
                    
            with open(os.path.dirname(__file__) +'/../../price.json','w')as file:
                file.write(json.dumps(self.obj))

            next_url = 'http://www.99acres.com' + response.xpath('//div[@class="pgdiv"]//a/@href').extract()[-1]
            yield scrapy.Request(next_url, callback=self.parse)
            return
        except :
            return