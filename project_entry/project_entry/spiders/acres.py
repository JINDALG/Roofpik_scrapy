import scrapy 
from pprint import pprint
import re
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

class acres99(scrapy.Spider):
	name = "99acres"
	allowed_domains = ["99acres.com"]   # target site
	start_urls = ['http://www.99acres.com/vipul-greens-sector-48-gurgaon-npxid-r12234?sid=UiB8IFFTIHwgUyB8IzcjICB8IENQMSB8IFkgIzE2I3wgIHwgMSM0IyB8IDEgfCA4ICM1I3wgIHwgMSMzNiMgfCA2NjgjNCMgfCA=']
	def __init__(self, filename=None):
		self.driver = webdriver.Chrome()
		dispatcher.connect(self.spider_closed, signals.spider_closed)

	def spider_closed(self, spider):
		self.driver.close()

	def parse(self,response):
		item = {}
		min_price = min_area = max_price = max_area = area =  -1
		status = apartment_type = apartment_bhk = "" 
		try :
			name = ''.join(response.xpath('//div[@class="bannerOver"]//span[@itemprop="name"]//text()').extract())
		except:
			name = ""
		
		try :
			facts = response.xpath('//div[@id="xidFactTable"]/div[contains(@class,"factBox")]')
			for fact in facts:
				try :
					head = ''.join(fact.xpath('div[contains(@class,"factData")]//div[contains(@class,"factLbl")]//text()').extract())
					if "Possession" in head:
						status =' '.join(fact.xpath('div[contains(@class,"factData")]//div[contains(@class,"factVal")]//text()').extract())
					
					if "Address" in head:
						addres =' '.join(fact.xpath('div[contains(@class,"factData")]//div[contains(@class,"factVal")]//text()').extract())
				
					if "Configuration" in head:
						apartment_type =''.join(fact.xpath('div[contains(@class,"factData")]//div[contains(@class,"factVal1")]//text()').extract())
						apartment_bhk = ''.join(fact.xpath('div[contains(@class,"factData")]//div[contains(@class,"factVal2")]//text()').extract()).replace('BHK','')
					
					if "Total Project Area" in head:
						area =''.join(fact.xpath('div[contains(@class,"factData")]//div[contains(@class,"factVal")]//text()').extract()).replace('Acres','')
						area  = float(area)
					
					if "Saleable Area" in head:
						areas = ''.join(fact.xpath('div[contains(@class,"factData")]//div[contains(@class,"factVal")]//text()').extract())
						areas = re.findall('\d+', areas)
						min_area = float(areas[0])
						max_area = float(areas[1])

					if "Resale Price" in head:
						price =''.join(fact.xpath('div[contains(@class,"factData")]//div[contains(@class,"factVal")]//text()').extract())
						price = (re.sub(r'[^\x00-\x7F]', " ", price))
						iscr = 'Crore' in price
						islac = 'Lac' in price
						price = price.replace('Crore','').replace('Lac','').split('to')
						min_price,max_price = map(float,price.split('to'))
						min_price *= 10000000 if iscr else 1
						max_price *= 10000000 if iscr else 1
						min_price *= 100000 if islac else 1
						min_price *= 100000 if islac else 1

					if "New Booking Base Price" in head:
						price =''.join(fact.xpath('div[contains(@class,"factData")]//div[contains(@class,"factVal")]//text()').extract())
						price = (re.sub(r'[^\x00-\x7F]', " ", price))
						iscr = 'Crore' in price
						islac = 'Lac' in price
						price = price.replace('Crore','').replace('Lac','').strip()
						min_price,max_price = map(float,price.split('to'))
						min_price *= 10000000 if iscr else 1
						max_price *= 10000000 if iscr else 1
						min_price *= 100000 if islac else 1
						min_price *= 100000 if islac else 1
				except:
					pass
		except :
			pass
		self.driver.get(response.url)
		amenity = []
		try :
			
			resp = TextResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
			basic = resp.xpath('//div[contains(@class,"Basic")]/div/div')
			for bas in basic:
				try :
					amen = ''.join(bas.xpath('div/text()').extract())
					print amen
					amenity += [amen.encode('utf8')]
				except:
					pass
		except :
			pass
		try :
			extras = resp.xpath('//div[@class="xidPrmAmn"]//li[not(@class)]/text()').extract()
			for extra in extras:
				try :
					amenity += [extra.encode('utf8')]
				except:
					pass
		except:
			pass

		det = []
		try :
			details = resp.xpath('//div[@class="elems-cs"]')
			for detail in details:
				try :
					try :
						bhk = ''.join(detail.xpath('div[@class="head"]/div//text()').extract())[0].encode('utf8')
					except :
						pass
					try :
						superbuiltarea = float(''.join(detail.xpath('div[2]/div[2]/text()').extract()))
					except :
						pass
					try :
						builtuparea = float(''.join(detail.xpath('div[5]/div[2]/text()').extract()))
					except :
						pass
					try :
						price =(''.join(detail.xpath('div[8]/div[2]/text()').extract()))
						price = (re.sub(r'[^\x00-\x7F]', " ", price))
						iscr = 'Crore' in price
						islac = 'Lac' in price
						price = price.replace('Crore','').replace('Lac','').strip().split('-')
						try :
							min_price = float(price[0])
						except:
							min_price  = 0
						try :
							max_price = float(price[1])
						except :
							max_price = 0
						min_price *= 10000000 if iscr else 1
						max_price *= 10000000 if iscr else 1
						min_price *= 100000 if islac else 1
						min_price *= 100000 if islac else 1
					except :
						pass
					det += [{'bhk':bhk,'min_price':min_price,'max_price':max_price,'superBuiltArea':superbuiltarea,'builtupArea':builtuparea,}]
				except :
					pass
		except :
			pass

		item['url'] = response.url
		item['name'] = name.encode('utf8')
		item['status'] = status.encode('utf8')
		item['type'] = apartment_type.encode('utf8')
		item['bhk'] = apartment_bhk.encode('utf8')
		item['area'] = area
		item['min_area'] = min_area
		item['max_area'] = max_area
		item['min_price'] = min_price
		item['max_price'] = max_price
		item['amenity'] = amenity
		item['address'] = addres.encode('utf8')
		item['detail'] = det
		pprint(item)