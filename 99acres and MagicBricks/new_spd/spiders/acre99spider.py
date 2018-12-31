#!usr/bin/python -tt
import scrapy 
from new_spd.items import NewSpdItem
import start_url_99acres
from pprint import pprint
import re
from new_spd.DBCreater import create_db
from month import find_month

class acres99Spider(scrapy.Spider):
    name = "acres99"
    allowed_domains = ["99acres.com"]   # target site
    #start_urls = start()
    #start_urls =["http://www.99acres.com/search/property/rent/residential-all/delhi-ncr-all?search_type=QS&search_location=CP1&lstAcn=CP_R&lstAcnId=1&src=CLUSTER&preference=R&selected_tab=4&city=1&res_com=R&property_type=R&isvoicesearch=N&keyword_suggest=delhi%20%2F%20ncr%20(all)%3B&class=A%2CO%2CB&fullSelectedSuggestions=delhi%20%2F%20ncr%20(all)&strEntityMap=W3sidHlwZSI6ImNpdHkifSx7IjEiOlsiZGVsaGkgLyBuY3IgKGFsbCkiLCJDSVRZXzEsIFBSRUZFUkVOQ0VfUiwgUkVTQ09NX1IiXX1d&texttypedtillsuggestion=Delhi&refine_results=Y&Refine_Localities=Refine%20Localities&action=%2Fdo%2Fquicksearch%2Fsearch&suggestion=CITY_1%2C%20PREFERENCE_R%2C%20RESCOM_R&searchform=1&price_max=null'"]
    
    def start_requests(self):
        url = start_url_99acres.start()
        #for url in urls:

        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        urls = response.xpath('//div[@class="wrapttl"]/div/a/@href').extract() 
        new_lst = response.xpath('//div[@class="wrapttl"]//text()').extract()   

        if len(urls) == 0:
            return
        for url in urls:
            abs_url = 'http://www.99acres.com' + url
            yield scrapy.Request(abs_url, callback=self.parse_property_info)
           
        next_url = 'http://www.99acres.com' + response.xpath('//div[@class="pgdiv"]//a/@href').extract()[-1]
        yield scrapy.Request(next_url, callback=self.parse)

    def parse_property_info(self, response):    
        # this function scrpaes info off the property page using xpaths
        # try except is used to avoid crashing in case of missing fields

        item = NewSpdItem()
        try :
            maintainance = posted_by_details = posted_on_date = project_name = price_per_unit = location = address = city =""
            carpet_area = super_built_area =  -1.0
            washroom = bedrooms = -1
            is_price_fixed = True
            price = -1.0
            try :
                super_built_area =  (''.join(response.xpath('//i[@id="superbuiltupArea_span"]//text()').extract()))
                super_built_area = float(re.findall('\d+', super_built_area)[0])
            except :
                super_built_area = -1.0

            try :
                carpet_area =  (''.join(response.xpath('//i[@id="builtupArea_span"]//text()').extract()))
                carpet_area = float(re.findall('\d+', carpet_area)[0])
            except :
                carpet_area = -1.0

            if carpet_area == "":
                try :
                    carpet_area =  (''.join(response.xpath('//i[@id="carpetArea_span"]//text()').extract()))
                    carpet_area = float(re.findall('\d+', carpet_area)[0])
                except :
                    carpet_area = -1.0

            try:
                price = (''.join(response.xpath('//span[@class="redPd b"]/text()').extract())).replace(',','').lower()
                islac = 'lac' in price
                iscr = 'cr' in price
                price = float(re.findall('\d+', price)[0])
                if(islac):
                    price = price * 100000
                if(iscr):
                    price = price * 10000000
            except:
                price = -1.0

            try :
                maintain = response.xpath('//div[@class="mb10"]//li')
                for main in maintain:
                    try :
                        if "Maintenance" in  ''.join(main.xpath('i//text()').extract()):
                            maintainance = (main.xpath('em/text()').extract()[-1]).replace('\n','')
                            maintainance = re.sub(' +',' ', maintainance)
                            break
                    except :
                        pass
            except :
                pass

            try:
                address = (''.join(response.xpath('//div[@id="AddTuplePd"]//text()').extract())).replace('Address:','').replace('\n','')
                address = re.sub(' +', ' ', address)
                city = address.split(',')[-2]
                location = address.split(',')[-3]          
            except:
                pass

            try:
                washroom = (response.xpath('//div[@class="lf"]/b//text()').extract()[0]).replace(':','')
                bedrooms = (''.join(response.xpath('//div[@id="bedroom_numLabel"]/b//text()   ').extract()[-1])).replace(':','')
                washroom = int(washroom)
                bedrooms = int(bedrooms)
            except:
                washroom = bathrooms = -1.0
                pass

            try:
                project_name = (''.join(response.xpath('//span[@class="addPdElip lf"]//text()').extract()[0])).replace('\n','')
                project_name = re.sub(' +',' ',project_name)
            except:
                pass
            
            try:
                posted_on_date = (''.join(response.xpath('//span[contains(@class,"PostdByPd")]//text()').extract())).replace('\n','').replace('Posted on:','').replace(',','')
                posted_on_date = posted_on_date.split()
                posted_on_date[0],posted_on_date[1] = posted_on_date[1],posted_on_date[0]
                posted_on_date[1] = find_month(posted_on_date[1])  
                posted_on_date[0] += "0" if len(posted_on_date) == 1 else ""
                posted_on_date  = '-'.join(posted_on_date[::-1])
                posted_on_date = re.sub(' +','',posted_on_date)    
            except:
                pass

            try:
                posted_by_details = (''.join(response.xpath('//a[@id="ContactPdBody"]/text()').extract())).replace('Contact','').replace('\n','')
                posted_by_details = re.sub(' +',' ',posted_by_details) # Remove 'Contact'
            except:
                pass

            try :
                temp = ''.join(response.xpath('//em/text()').extract())
                is_price_fixed = False if "Negotiable" in temp else True
            except :
                pass
            
            try :
                item['Price'] = price
                item['PricePerUnit'] = price_per_unit.encode('utf8')
                item['maintainance'] = maintainance.encode('utf8')
                item['is_price_fixed'] = is_price_fixed 

                item['SuperBuiltupArea'] = super_built_area
                item['CarpetArea'] = carpet_area

                item['city'] = city.encode('utf8')
                item['address'] = address.encode('utf8')
                item['Location'] = location.encode('utf8')
                
                item['Washroom'] = washroom

                item['PostedBy'] = posted_by_details.encode('utf8')
                item['PostingDate'] = posted_on_date.encode('utf8')
                item['ProjectName'] = project_name.encode('utf8')

                item['Bedrooms'] = bedrooms
                item['URL'] = response.url
                item['website']  = (response.url).split('/')[2]
                yield item
            except :
                yield NewSpdItem()
            
        except :
            yield item