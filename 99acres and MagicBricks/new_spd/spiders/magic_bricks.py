#!usr/bin/python -tt
import scrapy 
from new_spd.items import NewSpdItem
import start_url_magic
from pprint import pprint
import re
from month import find_month

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
        try :
            maintainance = posted_by_details = posted_on_date = project_name  = location = address = city =""
            carpet_area = super_built_area =  -1.0
            washroom = bedrooms = -1
            is_price_fixed = True
            price = price_per_unit = -1.0

            try:
                super_built_area_unit = ''.join(response.xpath('//div[@id="coveredAreaUnit"]//text()').extract())
            except:
                pass

            try:
                carpet_area_unit = ''.join(response.xpath('//div[@id="carpetAreaUnit"]//text()').extract())
            except:
                pass

            try:
                super_built_area = (''.join(response.xpath('//span[@id="coveredAreaDisplay"]//text()').extract())).replace(',','').replace('\n','')
                super_built_area = float(re.findall('\d+', super_built_area)[0])
                if "yrd" in super_built_area_unit:
                    super_built_area *= 9
            except:
                super_built_area = -1.0

            try:
                carpet_area = (''.join(response.xpath('//span[@id="carpetAreaDisplay"]//text()').extract())).replace(',','').replace('\n','')
                carpet_area = float(re.findall('\d+', carpet_area)[0])
                if "yrd" in carpet_area_unit:
                    carpet_area *= 9
            except:
                carpet_area = -1.0
            

            try :
                datalist = response.xpath("//div[@class='nMoreListData']/div[@class='nDataRow']")
                for data in datalist:
                    try :
                        label = data.xpath('div[@class="dataLabel"]//text()').extract()[0]
                        if "Rent" in label:
                            try :
                                price = ((data.xpath('div[@class="dataVal"]/span[contains(@class,"fBold")]//text()').extract())[0].split())[-1].replace(',','').lower()
                                price = float(''.join(ele for ele in price if ele.isdigit() or ele == '.'))
                            except:
                                price = -1.0

                            try:
                                price_per_unit = ((data.xpath('div[@class="dataVal"]/span[@class="light"]/text()').extract())[1].split())[1]
                                priceunit = ((data.xpath('div[@class="dataVal"]/span[@class="light"]//text()').extract())[1].split())[3].strip()
                                price_per_unit = float(''.join(ele for ele in price_per_unit if ele.isdigit() or ele == '.'))
                                if "sqyrd" in priceunit:
                                    price_per_unit *= 9
                                
                            except:
                                price_per_unit = -1.0

                        if "Address" in label:
                            try :
                                address = ''.join(data.xpath('div[@class="dataVal"]/text()').extract()).replace('\n','')
                            except:
                                pass

                    except :
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
            
            try :
                if address == '':
                    address = location + city
            except :
                pass

            try :
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
                                    try :
                                        info  = info.replace('\n',' ')
                                        if "Bathroom" in info:
                                            info = (info.strip().split())[0]
                                            washroom = int(info)
                                    except :
                                        pass
                            except:
                                pass
                    except:
                        pass
            except :
                pass

            try:
                posted_on_date = ((((response.xpath('//div[@class="propIDnPDate"]//text()').extract())[0].split('|'))[1]).split(':'))[1]
                posted_on_date = posted_on_date.replace(',',' ').replace('\'',' ')
                posted_on_date = re.sub(' +',' ',posted_on_date) 
                posted_on_date = posted_on_date.split()
                posted_on_date[0],posted_on_date[1] = posted_on_date[1],posted_on_date[0]
                posted_on_date[1] = find_month(posted_on_date[1])  
                posted_on_date[0] += "0" if len(posted_on_date) == 1 else ""
                posted_on_date  = '-'.join(posted_on_date[::-1])
            except:
                pass


            try :
                project_name = (''.join(response.xpath('//div[@class="nProjNmLoc"]/a//text()').extract())).replace('\n','')

            except :
                pass

            try:
                posted_by_details = ''.join(response.xpath('//a[contains(@id,"agentBtn")]//text()').extract()[0]).replace('Contact ','') # Remove 'Contact'
                
            except:
                pass
            try :
                item['URL'] = response.url
                item['website']  = (response.url).split('/')[2]
                item['Price'] = price
                item['PricePerUnit'] = price_per_unit
                item['maintainance'] = maintainance.encode('utf8')
                item['is_price_fixed'] = is_price_fixed
            
                item['SuperBuiltupArea'] = super_built_area
                item['CarpetArea'] = carpet_area

                item['city'] = city.encode('utf8')
                item['address'] = address.encode('utf8')
                item['Location'] = location.encode('utf8')
                
                item['Washroom'] = washroom
                item['Bedrooms'] = bedrooms

                item['PostedBy'] = posted_by_details.encode('utf8')
                item['PostingDate'] = posted_on_date.encode('utf8')
                item['ProjectName'] = project_name.encode('utf8')
                
                if project_name == '':
                    print response.url
                    print "\n\n\nproject name missing\n\n\n"
                    yield
                else :
                    pprint(item)
                    yield item
            except :
                print "error1"
                yield            
        except :
            print "error2"
            yield
