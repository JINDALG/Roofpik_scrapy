#!usr/bin/python -tt
import scrapy 
from new_spd.items import NewSpdItem
import start_url_99acres
from pprint import pprint
import re
from new_spd.DBCreater import create_db

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
        posted_by_details = posted_on_date = project_name = price_per_unit = availability = location = address = description = ''
        area1 = area2 = area3 = area4 = ''
        area = washroom = bedrooms = -1
        price = -1.0
        try:
            area1 = ''.join(response.xpath('//i[@id="builtupArea_span"]//text()').extract()).strip() + ' '
        except:
            pass


        try:
            area2 = ''.join(response.xpath('//span[@class="lf mt5"]//text()').extract()).strip() + ' '
        except:
            pass


        try:
            area3 = ''.join(response.xpath('//b[@id="superArea_span"]//text()').extract()).strip() + ' '
        except:
            pass

        try:
            area4 = ''.join(response.xpath('//i[@id="areaRange"]//text()').extract()).strip() 
        except:
            pass

        superBuiltupArea = builtupArea = carpetArea = ''
        try:
            area = ''.join((area1 + area2 + area3 + area4).replace(' ', '' ).split(':')).replace('\n', '').lower()
            area = area.replace('-', '').replace('.00', '').replace(',', '')

            try:
                superBuiltupArea = area.split('superbuiltuparea')[1]
                superBuiltupArea = map(int, re.findall('\d+', superBuiltupArea))[0]
                superBuiltupArea = float(superBuiltupArea)

            except:
                pass

            if (not 'superbuiltuparea' in area and 'builtuparea' in area):
                builtupArea = area.split('builtuparea')[1]
                builtupArea = map(int, re.findall('\d+', builtupArea))[0]

            if('carpetarea' in area):
                carpetArea = area.split('builtuparea')[1]
                carpetArea = map(int, re.findall('\d+', carpetArea))[0]                


        except:
            pass

        try:
            price = ((response.xpath('//span[@class="redPd b"]//text()').extract())[-1].strip()).replace(',', '').lower()
            islac = 'lac' in price
            iscr = 'cr' in price
            price = float(''.join(ele for ele in price if ele.isdigit() or ele == '.'))
            if(islac):
                price = price * 100000
            if(iscr):
                price = price * 10000000
        except:
            pass

        try:
            availability = response.xpath('//i[@class="blk"]//text()').extract()[-1][1:]
            #price_per_unit = response.xpath('//span[@class="rf PostdByPd mt3 f13 "]//text()').extract()[0].strip() + ' Per sq ft'
        except:
            pass

        try:
            location = response.xpath('//h1[@class="prop_seo_head f16 b"]//text()').extract()
            address = location[1].strip()
            location = location[0].strip()
            city =  location.split(',')
            city = city[-1].strip()
            city = city.replace(' ','_')            
        except:
            pass

        try:
            washroom = response.xpath('//div[@class="lf"]/b//text()').extract()[0][2:]
            bedrooms = ''.join(response.xpath('//div[@id="bedroom_numLabel"]//text()').extract()).replace('  ', '')[12:]
            washroom = int(washroom)
            bedrooms = int(bedrooms)
        except:
            pass

        try:
            description = response.xpath('//div[@class="leftPane f13"]//p//text()').extract()[0].strip()
            project_name = response.xpath('//span[@class="addPdElip lf"]//text()').extract()[0]
        except:
            pass

        try:
            price_per_unit = ''.join(response.xpath('//span[@class="bsp"]//text()').extract()).replace('  ', '')
        except:
            pass
        
        try:
            posted_on_date = response.xpath('//span[@class="rf PostdByPd mt3 f13 "]//text()').extract()[0][10:]
        except:
            pass

        try:
            posted_on_date = response.xpath('//span[@class="rf PostdByPd mt3 f13 blk"]//text()').extract()[0][10:]
        except:
            pass

        try:
            posted_by_details = response.xpath('//input[@id="contactPdBand"]/@value').extract()[0][7:] # Remove 'Contact'
            posted_by_details += ':' + response.xpath('//span[@class="grey f13"]//text()').extract()[0][9:] #remove 'Posted By:'
        except:
            pass

        property_age = property_info = booking_details = booking_amt = maintainance = brokerage = ''
        booking_details_tag = trends = additional_info = property_info_tags = ''
        try:
            property_info = response.xpath('//i[@class="blk"]//text()').extract()
            property_info_tags = response.xpath('//div[@class="spdp_blCny f13 fwn"]//text()').extract()

            #cleaning tags
            cleaned_tags = []
            for tag in property_info_tags:
                cleaned = tag.replace(' ','').replace('\n','').replace('\t','')
                if(cleaned != ''):
                    cleaned_tags.append(tag.replace('  ','').replace('\n','').replace('\t', ''))

            property_info_tags = []
            prev = ''
            for tag in cleaned_tags:
                if(tag[0] == ':'):
                    property_info_tags.append(prev + tag)
                prev = tag
                property_info_tags = ', '.join(property_info_tags)


        except:
            pass

        booking_info = []
        booking_price = main_amt = deposit = brokerage = -1
        gated = additional_rooms = flooring = power_backup = ''
        try:    
            booking_details = (response.xpath('//div[@class="lf"]//li/em/text()').extract())
            booking_details_tag = response.xpath('//div[@class="lf"]//li/i//text()').extract()
            booking_info = []
            cleaned_details = []
            prev = ''
            for line in booking_details:
                cleaned = line.replace(':', '').replace(' ', '').replace('\n','')
                if(cleaned != '' and cleaned != 'Rs.' and cleaned != u'\u20b9'):
                    if(cleaned[-1] == '('):
                        prev = cleaned
                    else:
                        cleaned_details.append(prev + line.replace(':', ''))
                        prev = ''

            for i in range(0, len(cleaned_details)):
                booking_info.append(booking_details_tag[i] + ':' +  cleaned_details[i])

            for data in booking_info:
                filtered = data.replace(' ', '').replace(',','').lower()
                try:
                    number = float(''.join(ele for ele in data if ele.isdigit() or ele == '.'))
                except:
                    pass

                islac = False


                if ('lac' in data.lower()):     islac = True    # check if amt is entered in lacs

                if('bookingamount' in filtered):
                    booking_price = int(number)
                    if(islac):  booking_price *= 100000
                elif('maintenance' in filtered):
                    main_amt = int(number)
                    if(islac):  maintenance *= 100000

                elif('room' in filtered):
                    additional_rooms = data.split(':')[1].replace(',', ', ')

                elif('gated' in filtered):
                    gated = data.split(':')[1]

                elif('power' in filtered):
                    power_backup = data.split(':')[1]

                elif('deposit' in filtered):
                    number = float(''.join(ele for ele in data.split('(')[-1] if ele.isdigit() or ele == '.'))
                    deposit = int(number)
                    if(islac):  deposit *= 100000

            booking_info = ', '.join(booking_info)

        except:
            pass 

        views = searched = 0
        property_code = ''
        try:
            views = ''.join(response.xpath('//div[@class="lf hp5 vp15 lh18"]//text()').extract()).replace('  ', '').replace('\n', '').replace('\t', '')
            property_code = response.xpath('//div[@class="lf hp5 mt12  grey"]//text()').extract()[0][15:]

            #cleaning
            views_new = [int(s) for s in views.split() if s.isdigit()]
            searched = int(views_new[1])
            views = int(views_new[0])

        except:
            pass

        trends_tags = raw_tags = raw_trends = ''
        trending_table = ''
        try: 
            raw_trends = response.xpath('//div[@id="prContainerRent"]//table//tr//text()').extract()
            raw_tags = response.xpath('//div[@id="prContainerRent"]//table//tr[@class]//text()').extract()
            trends_tags = []
            
            for data in raw_tags:
                cleaned = data.replace('\t','').replace('\n','').replace(' ','')
                if(cleaned != ''):
                    trends_tags.append(data)

            i = 0
            size = len(trends_tags)
            temp = []
            trending_table = []

            for data in raw_trends:
                cleaned = data.replace('\t','').replace('\n','').replace(' ', '')
                if(i == size):
                    i = 0
                    if(len(temp) == 2) :
                        temp.append('-')
                        temp.append('-')
                    if(len(temp) == 3):
                        temp.append('-')
                    if(len(temp) > 4):
                        temp = temp[:4]

                    temp = ('_ABC_'.join(temp))
                    trending_table.append(temp)
                    temp = []
                if(data != 'Rs.' and cleaned != ''):
                    i +=1
                    temp.append(cleaned)

            trending_table = trending_table[1:]
            trending_table = ('_XYZ_'.join(trending_table))
            #print '\n\n\n\n\n\n\n' , trending_table, '\n\n\n\n\n\n'
        except:
            pass
        
        furnishing = ''
        try:
            furnishing = response.xpath('//label[@style="font-size:13px;"]//text()').extract()[0]
        except:
            pass

        questions = ''
        try:
            raw_questions = (response.xpath('//div[@class="ml10pdb5 f12"]//span//text()').extract())
            questions = []
            i = 0
            for line in raw_questions:
                cleaned = line.replace('\n', '').replace('  ', '')
                if(len(cleaned) >= 20):
                    questions.append(cleaned)
        except:
            pass
        
        item['Price'] = price
        item['PricePerUnit'] = price_per_unit.encode('utf8')

        item['Availability'] = availability.encode('utf8')
        item['SuperBuiltupArea'] = superBuiltupArea
        item['BuiltupArea'] = builtupArea
        item['CarpetArea'] = carpetArea

        item['city'] = city.encode('utf8')
        item['address'] = address.encode('utf8')
        item['Location'] = location
        
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
