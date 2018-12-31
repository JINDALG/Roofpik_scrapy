from buy.items import BuyItem
import start_url
from pprint import pprint
import re
import month
import scrapy

class magic(scrapy.Spider):
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
        urls = response.xpath('//div[@class="proNameColm1"]/p/a/@href').extract() 
        pprint(urls)
        #urls=['http://www.magicbricks.com/propertyDetails/270-Sq-ft-Studio-Apartment-FOR-Sale-Vatika-City-in-Gurgaon&id=4d423230333337333839?from=search']
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

        try :
            full_price = ''.join(response.xpath('//div[@class="nActualAmt"]//text()').extract())
            price = float(full_price.split()[1])
            if "Lac" in full_price:
                price *= 100000
            if "Cr" in full_price:
                price  *= 1000000
        except :
            pass

        try :
            SuperBuiltupArea = float(''.join(response.xpath('//span[@id="coveredAreaDisplay"]//text()').extract()))
        except :
            pass

        try :
            min_area = max_area = float(''.join(response.xpath('//span[@id="carpetAreaDisplay"]//text()').extract()))
        except :
            pass


        datalist = response.xpath("//div[@class='nMoreListData']/div[@class='nDataRow']")
        for data in datalist:
            try :
                label = data.xpath('div[@class="dataLabel"]//text()').extract()[0]
                if "Price" in label:
                    try :
                        if price == 0.0:
                            price = ((data.xpath('div[@class="dataVal"]/span[contains(@class,"fBold")]//text()').extract())[0].split())[-1].replace(',','').lower()
                            price = float(''.join(ele for ele in price if ele.isdigit() or ele == '.'))
                    except:
                        pass

                    try:
                        price_per_sqft = ((data.xpath('div[@class="dataVal"]/span[@class="light"]/text()').extract())[1].split())[1]
                        priceunit = ((data.xpath('div[@class="dataVal"]/span[@class="light"]//text()').extract())[1].split())[3].strip()
                        price_per_sqft = float(''.join(ele for ele in price_per_sqft if ele.isdigit() or ele == '.'))
                        if "sqyrd" in priceunit:
                            price_per_sqft *= 9
                        
                    except:
                        pass

                if "Address" in label:
                    try :
                        address = ''.join(data.xpath('div[@class="dataVal"]//text()').extract()).replace('\n','').replace('\t','')
                    except:
                        pass

                if "Water Availability" in label:
                    try :
                        speciality[label] = ''.join(data.xpath('div[@class="dataVal"]//text()').extract()).replace('\n','').replace('\t','')
                        
                    except:
                        pass
                if "Status of Electricity" in label:
                    try :
                        speciality[label] = ''.join(data.xpath('div[@class="dataVal"]//text()').extract()).replace('\n','').replace('\t','')
                        
                    except:
                        pass

                if "Flooring" in label:
                    try :
                        speciality[label] = ''.join(data.xpath('div[contains(@class,"dataVal")]//text()').extract()).replace('\n','').replace('\t','')
                    except:
                        pass
            except :
                pass

        try :
            if address == "":
                address =  (''.join(response.xpath('//div[@class="nProjNmLoc"]//text()').extract())).replace('\n','').replace('\t','')
        except:
            pass

        try :
            location = ''.join(response.xpath('//span[@itemprop="streetAddress"]//text()').extract()).replace(',',' ')
        except :
            pass

        try:
            city = ''.join(response.xpath('//span[@itemprop="addressLocality"]//text()').extract()).replace(',',' ')
        except:
            pass

        try :
            if address == "":
                address =  location + ' ' +  city
        except:
            pass
        if city == '':
            try :
                city = address.split(',')[-1]
            except :
                pass

        if location == '':
            try :
                location = address.split(',')[-2]
            except :
                pass
        datalist = response.xpath('//div[@class="nInfoDataBlock"]/div[@class="nDataRow"]')
        for data in datalist:
            try :
                label = ''.join(data.xpath('div[@class="dataLabel"]//text()').extract())
                if "Configuration" in label :
                    try :
                        bedrooms = int(((data.xpath('div[@class="dataVal"]/span//text()').extract())[0].split())[0])
                    except :
                        pass
                    try :
                        other = (''.join(data.xpath('div[@class="dataVal"]/text()').extract())).split(",")
                        
                        for info in other:
                            info  = info.replace('\n',' ')
                            if "Bathroom" in info:
                                info = (info.strip().split())[0]
                                bathrooms = int(info)
                            if "Room" in info:
                                speciality['addional_room'] = info.strip()
                    except:
                        pass

                if "Transaction" in label:
                    try :
                        temp = ''.join(data.xpath('div[@class="dataVal"]//text()').extract()).strip()
                        if "Resale" in temp:
                            is_resale = 1
                    except :
                        pass

                if "Status" in label:
                    try :
                        status = (''.join(data.xpath('div[@class="dataVal"]//text()').extract())).replace('\n','')
                        if status  =='':
                            status = (''.join(data.xpath('li/div[@class="dataVal"]//text()').extract())).replace('\n','')
                    except :
                        pass

                if "Age" in label:
                    try :
                        age_of_property = (''.join(data.xpath('div[@class="dataVal"]//text()').extract())).replace('\n','')
                        if age_of_property=='' :
                            age_of_property = (''.join(data.xpath('li/div[@class="dataVal"]//text()').extract())).replace('\n','')
                    except :
                        pass

                if "Furnish" in label:
                    try :
                        speciality['furnishing'] = ''.join(data.xpath('div[@class="dataVal"]//text()').extract()).strip()
                    except :
                        pass

                if "Car Parking" in label:
                    try :
                        speciality['parking'] = ''.join(data.xpath('div[@class="dataVal"]//text()').extract()).strip()
                    except :
                        pass
            except:
                pass

        try:
            description = ''.join(response.xpath("//span[@class='dDetail']//text()").extract()).replace('\n','')
        except:
            pass

        if description == "":
            try :
                description = (''.join(response.xpath("//div[@class='nAboutBrf']//text()").extract())).replace('\n','').replace('\t','')
            except :
                pass

        try:
            posted_on_date = ((((response.xpath('//div[@class="propIDnPDate"]//text()').extract())[0].split('|'))[1]).split(':'))[1].strip().replace(',',' ')
            posted_on_date = posted_on_date.split()
            posted_on_date[0],posted_on_date[1] = posted_on_date[1],posted_on_date[0]
            posted_on_date[1] = month.find_month(posted_on_date[1])
            posted_on_date = ' '.join(posted_on_date)
        except:
            pass

        try:
            code = (((response.xpath('//div[@class="propIDnPDate"][1]//text()').extract())[0].split("|"))[0].split(":"))[1].strip()
            
        except:
            pass 

        try:
            agent_name = response.xpath('//div[@class="agntName"]//text()').extract()[-1] # Remove 'Contact'
            
        except:
            pass

        amenities = ','.join(response.xpath('//div[@id="normalAminities"]//li[not(@class="notAvail")]/span[@class="ameLabel"]/text()').extract())

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
        item['posted_on']  = posted_on_date.encode('utf8')
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

