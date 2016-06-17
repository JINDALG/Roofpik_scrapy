#!usr/bin/python -tt
import scrapy 
from new_spd.items import NewSpdItem
import start_url_magic
from pprint import pprint
import re

class acres99Spider(scrapy.Spider):
    page = 1
    name = "mbricks"
    allowed_domains = ["magicbricks.com"]   # target site
    #start_urls = start()
    #start_urls =["http://www.99acres.com/search/property/rent/residential-all/delhi-ncr-all?search_type=QS&search_location=CP1&lstAcn=CP_R&lstAcnId=1&src=CLUSTER&preference=R&selected_tab=4&city=1&res_com=R&property_type=R&isvoicesearch=N&keyword_suggest=delhi%20%2F%20ncr%20(all)%3B&class=A%2CO%2CB&fullSelectedSuggestions=delhi%20%2F%20ncr%20(all)&strEntityMap=W3sidHlwZSI6ImNpdHkifSx7IjEiOlsiZGVsaGkgLyBuY3IgKGFsbCkiLCJDSVRZXzEsIFBSRUZFUkVOQ0VfUiwgUkVTQ09NX1IiXX1d&texttypedtillsuggestion=Delhi&refine_results=Y&Refine_Localities=Refine%20Localities&action=%2Fdo%2Fquicksearch%2Fsearch&suggestion=CITY_1%2C%20PREFERENCE_R%2C%20RESCOM_R&searchform=1&price_max=null'"]
    
    def start_requests(self):
        urls = start_url_magic.start()
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
        # this function scrpaes info off the property page using xpaths
        # try except is used to avoid crashing in case of missing fields
        item = NewSpdItem()
        booking_info = ""
        booking_price = main_amt = deposit = brokerage = views = searched = -1
        gated = additional_rooms = flooring = power_backup = city = trending_table =property_code = ''
        additional_rooms = flooring = power_backup = property_info_tags  =''
        posted_by_details = posted_on_date = project_name = price_per_unit = availability = location = address = description =furnishing =  ''
        area1 = area2 = area1unit = area2unit = ''
        area = washroom = bedrooms = -1
        price = -1.0
        try:
            area1 = ''.join(response.xpath('//div[@class="unitBlockArea"][1]/span[contains(@class,"fBold")]//text()').extract()).strip()
        except:
            pass

        try:
            area2 = ''.join(response.xpath('//div[@class="unitBlockArea"][2]/span[contains(@class,"fBold")]//text()').extract()).strip() + ' '
        except:
            pass

        try:
            area1unit = ''.join(response.xpath('//div[@class="unitBlockArea"][1]/div[contains(@id,"AreaUnit")]//text()').extract()).strip() + ' '
        except:
            pass

        try:
            area2unit = ''.join(response.xpath('//div[@class="unitBlockArea"][2]/div[contains(@id,"AreaUnit")]//text()').extract()).strip() 
        except:
            pass

        superBuiltupArea = builtupArea = carpetArea = ''
        try:
            # area = ''.join((area1 + area2 + area3 + area4).replace(' ', '' ).split(':')).replace('\n', '').lower()
            # area = area.replace('-', '').replace('.00', '').replace(',', '')

            try:
                superBuiltupArea = area1.split()[0]
                superBuiltupArea = map(int, re.findall('\d+', superBuiltupArea))[0]
                superBuiltupArea = float(superBuiltupArea)
                if "sqyrd" in area1unit:
                    superBuiltupArea *= 9
            except:
                pass

            # if (not 'superbuiltuparea' in area and 'builtuparea' in area):
            #     builtupArea = area.split('builtuparea')[1]
            #     builtupArea = map(int, re.findall('\d+', builtupArea))[0]

            try :
                carpetArea = area2.split()[0]
                carpetArea = map(int, re.findall('\d+', carpetArea))[0]                
                carpetArea = float(carpetArea)
                if "sqyrd" in area2unit:
                    carpetArea *= 9
            except :
                pass

        except:
            pass
        datalist = response.xpath("//div[@class='nMoreListData']/div[@class='nDataRow']")
        for data in datalist:
            try :
                label = data.xpath('div[@class="dataLabel"]//text()').extract()[0]
                if "Rent" in label:
                    try :
                        price = ((data.xpath('div[@class="dataVal"]/span[contains(@class,"fBold")]//text()').extract())[0].split())[-1].replace(',','').lower()
                        price = float(''.join(ele for ele in price if ele.isdigit() or ele == '.'))
                    except:
                        pass

                    try:
                        price_per_unit = ((data.xpath('div[@class="dataVal"]/span[@class="light"]/text()').extract())[1].split())[1]
                        priceunit = ((data.xpath('div[@class="dataVal"]/span[@class="light"]//text()').extract())[1].split())[3].strip()
                        price_per_unit = float(''.join(ele for ele in price_per_unit if ele.isdigit() or ele == '.'))
                        if "sqyrd" in priceunit:
                            price_per_unit *= 9
                        price_per_unit = str(price_per_unit)
                        
                    except:
                        pass

                    try :
                        booking_info = ''.join(data.xpath('div[@class="dataVal"]/div//text()').extract()).replace('\n',' ')
                        booking_info  = (''.join([i if ord(i) < 128 else ' ' for i in booking_info])).strip()
                    except :
                        pass

                if "Tenants" in label:
                    try :
                        availability = ''.join(data.xpath('div[@class="dataVal"]//text()').extract()).replace('\n','')
                    except:
                        pass

                if "Address" in label:
                    try :
                        address = ''.join(data.xpath('div[@class="dataVal"]//text()').extract()).replace('\n','')
                    except:
                        pass

                if "Electricity" in label:
                    try :
                        power_backup = ''.join(data.xpath('div[@class="dataVal"]//text()').extract()).strip()
                    except:
                        pass

            except :
                pass

        try :
            location = ''.join(response.xpath('//span[@itemprop="streetAddress"]//text()').extract()).replace(',',' ')
        except :
            pass

        try:
            city = ''.join(response.xpath('//span[@itemprop="addressLocality"]//text()').extract()).replace(',',' ')
        except:
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
                        other = ''.join(data.xpath('div[@class="dataVal"]/text()').extract()).split(",")
                        
                        for info in other:
                            info  = info.replace('\n',' ')
                            if "Bathroom" in info:
                                info = (info.strip().split())[0]
                                washroom = int(info)
                            if "Room" in info:
                                additional_rooms = info.strip()
                    except:
                        pass

                if "Furnish" in label:
                    try :
                        furnishing = ''.join(data.xpath('div[@class="dataVal"]//text()').extract()).strip()
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
                description = ''.join(response.xpath("//div[@class='nAboutBrf']//text()").extract())
            except :
                pass
        
        try:
            posted_on_date = ((((response.xpath('//div[@class="propIDnPDate"]//text()').extract())[0].split('|'))[1]).split(':'))[1].strip()
        except:
            pass

        try:
            property_code = (((response.xpath('//div[@class="propIDnPDate"][1]//text()').extract())[0].split("|"))[0].split(":"))[1].strip()
            
        except:
            pass    

        try:
            posted_by_details = response.xpath('//div[@class="agntName"]//text()').extract()[-1] # Remove 'Contact'
            
        except:
            pass

        questions = []
        
        item['Price'] = price
        item['PricePerUnit'] = price_per_unit.encode('utf8')

        item['Availability'] = availability.encode('utf8')
        item['SuperBuiltupArea'] = superBuiltupArea
        item['BuiltupArea'] = builtupArea
        item['CarpetArea'] = carpetArea

        item['city'] = city.encode('utf8')
        item['address'] = address.encode('utf8')
        item['Location'] = location.encode('utf8')
        
        item['Washroom'] = washroom
        item['Description'] = description.encode('utf8')

        item['PostedBy'] = posted_by_details.encode('utf8')
        item['PostingDate'] = posted_on_date.encode('utf8')
        item['ProjectName'] = project_name.encode('utf8')

        item['Bedrooms'] = bedrooms
        item['Views'] = views
        item['Searched'] = searched
        item['URL'] = response.url.encode('utf8')
            
        item['Question'] = ('__'.join(questions)).encode('utf8')

        item['Trends'] = trending_table.encode('utf8')
        item['PROPERTYCODE'] = property_code.encode('utf8')
        item['BookingAmount'] = booking_price
        item['Deposit'] = deposit
        item['GatedCommunity'] = gated.encode('utf8')
        item['PowerBackup'] = power_backup.encode('utf8')

        item['BookingINFO'] = booking_info.encode('utf8')
        item['AdditionalRooms'] = additional_rooms.encode('utf8')

        item['PropertyInfo'] = property_info_tags.encode('utf8')
        item['maintainance'] = main_amt
        item['Furnishing'] = furnishing.encode('utf8')
        # item_temp =  {
        #     'Price' : price, 'PricePerUnit' : price_per_unit.encode('utf8'), 'Availability' : availability,
        #     'SuperBuiltupArea' : superBuiltupArea, 'BuiltupArea': builtupArea, 'CarpetArea': carpetArea,
        #     'address': address, 'Location' : location, 'Washroom' : washroom, 'Description' : description,
        #     'PostedBy': posted_by_details, 'PostingDate' : posted_on_date, 'ProjectName' : project_name,
        #     'Bedrooms': bedrooms,  
        #     'Views' : views,'Searched' : searched, 'URL' : response.url,
        #     'Question' : questions,
        #     #'Trends': trending_table,
        #     'PROPERTYCODE' : property_code,'BookingAmount' : booking_price, 'Deposit': deposit, 
        #     'GatedCommunity' : gated, 'PowerBackup' : power_backup,
        #     'BookingINFO': booking_info, 'AdditionalRooms': additional_rooms,
        #     'PropertyInfo' : property_info_tags,'maintainance': main_amt,
        #     'Furnishing' : furnishing
        # }

        #print '\n\n\n\n\n\n', trending_table , '\n\n\n\n\n\n\n\n'
        #for key in item:    if(item[key] == ''):        item[key] = None
        yield item
