import scrapy 
from pprint import pprint
import re
import traceback
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
from read_json_acres import convert

class acres99(scrapy.Spider):
	name = "99acres"
	allowed_domains = ["99acres.com"]   # target site
	start_urls = None
	def __init__(self, filename=None):
		with open(os.path.dirname(__file__) + '/../../link.txt','r') as f:
			self.start_urls = [f.read()]
		self.driver = webdriver.Chrome()
		dispatcher.connect(self.spider_closed, signals.spider_closed)

	def spider_closed(self, spider):
		self.driver.close()

	def parse(self,response):
		item = {}
		min_booking_price = min_area = max_booking_price = max_area = area = max_resale_price = min_resale_price= -1
		status = apartment_type = apartment_bhk = project_detail= builderName= address ="" 
		superBuiltupArea = builtupArea = min_book_price = max_book_price = min_sale_price = max_sale_price = bhk = -1
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
						status =' '.join(fact.xpath('div[contains(@class,"factData")]//div[contains(@class,"factVal1")]//text()').extract())
					
					if "Address" in head:
						address =' '.join(fact.xpath('div[contains(@class,"factData")]//div[contains(@class,"factVal")]//text()').extract())
				
					if "Configuration" in head:
						apartment_type =''.join(fact.xpath('div[contains(@class,"factData")]//div[contains(@class,"factVal1")]//text()').extract())
						apartment_bhk = ''.join(fact.xpath('div[contains(@class,"factData")]//div[contains(@class,"factVal2")]//text()').extract()).replace('BHK','')
					
					if "Total Project Area" in head:
						area =''.join(fact.xpath('div[contains(@class,"factData")]//div[contains(@class,"factVal")]//text()').extract()).replace('Acres','')
						area  = float(area)*43560
					
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
						price = price.replace('Crore','').replace('Lac','').strip()
						min_resale_price,max_resale_price = map(float,price.split('to'))
						min_resale_price *= 10000000 if iscr else 1
						max_resale_price *= 10000000 if iscr else 1
						min_resale_price *= 100000 if islac else 1
						min_resale_price *= 100000 if islac else 1

					if "New Booking Base Price" in head:
						price =''.join(fact.xpath('div[contains(@class,"factData")]//div[contains(@class,"factVal")]//text()').extract())
						price = (re.sub(r'[^\x00-\x7F]', " ", price))
						iscr = 'Crore' in price
						islac = 'Lac' in price
						price = price.replace('Crore','').replace('Lac','').strip()
						min_booking_price, max_booking_price = map(float,price.split('to'))
						min_booking_price *= 10000000 if iscr else 1
						max_booking_price *= 10000000 if iscr else 1
						min_booking_price *= 100000 if islac else 1
						min_booking_price *= 100000 if islac else 1

					if "Project Details" in head:
						project_detail =' '.join(fact.xpath('div[contains(@class,"factData")]//div[contains(@class,"factVal")]//text()').extract())
						project_detail = (re.sub(r'[^\x00-\x7F]', " ", project_detail))
						
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
						bhk = int(bhk.replace('BHK Apartment',''))
					except :
						pass

					more_det = detail.xpath('div[@class="unit-d-cs"]')
					for internal_det in more_det:
						try :
							if "super built-up area" in ''.join(internal_det.xpath('div[1]/text()').extract()):
								superBuiltupArea = (''.join(internal_det.xpath('div[2]/text()').extract())).encode('utf8')

							if "Built-up area" in ''.join(internal_det.xpath('div[1]/text()').extract()):
								builtupArea = (''.join(internal_det.xpath('div[2]/text()').extract())).encode('utf8')

							if "New Booking Base Price" in ''.join(internal_det.xpath('div[1]/text()').extract()):
								price = (''.join(internal_det.xpath('div[2]/text()').extract()))
								iscr = 'Crore' in price
								islac = 'Lac' in price
								price = price.replace('Crore','').replace('Lac','')
								if '-' in price:
									price = price.split('-')
									min_book_price = float(price[0])
									max_book_price = float(price[1])
								else :
									min_book_price = max_book_price = float(price)
								min_book_price *= 10000000 if iscr else 1
								max_book_price *= 10000000 if iscr else 1
								min_book_price *= 100000 if islac else 1
								max_book_price *= 100000 if islac else 1

							if "Resale Price" in ''.join(internal_det.xpath('div[1]/text()').extract()):
								price = (''.join(internal_det.xpath('div[2]/text()').extract()))
								iscr = 'Crore' in price
								islac = 'Lac' in price
								price = price.replace('Crore','').replace('Lac','')
								if '-' in price:
									price = price.split('-')
									min_sale_price = float(price[0])
									max_sale_price = float(price[1])
								else :
									min_sale_price = max_sale_price = float(price)
								min_sale_price *= 10000000 if iscr else 1
								max_sale_price *= 10000000 if iscr else 1
								min_sale_price *= 100000 if islac else 1
								max_sale_price *= 100000 if islac else 1
						except:
							pass
					det += [{'bhk':bhk,
					'superBuiltupArea':superBuiltupArea,
					'builtupArea':builtupArea,
					'min_book_price':min_book_price,
					'max_book_price':max_book_price,
					'min_sale_price':min_sale_price,
					'max_sale_price':max_sale_price}]
				except :
					pass
		except :
			pass

		try :
			builderName = ''.join(resp.xpath('//span[@id="item_manufacturer"]//text()').extract())
		except :
			pass
		item['url'] = response.url
		item['projectName'] = name.encode('utf8')
		item['status'] = status.encode('utf8')
		item['projectType'] = apartment_type.encode('utf8')
		item['bhk'] = apartment_bhk.encode('utf8')
		item['area'] = area
		item['min_area'] = min_area
		item['max_area'] = max_area
		item['min_booking_price'] = min_booking_price
		item['max_booking_price'] = max_booking_price
		item['min_resale_price'] = min_resale_price
		item['max_resale_price'] = max_resale_price
		item['amenity'] = amenity
		item['address'] = address.encode('utf8')
		item['units'] = det
		item['website']  = (response.url).split('/')[2].split('.')[1]
		item['project_detail'] = project_detail.encode('utf8')
		item['builderName'] = builderName.encode('utf-8')

		try :
			item = convert(item)
		except :
			print traceback.print_exc()
			item = {}
		fire = firebase.FirebaseApplication('https://abcapp-8345a.firebaseio.com/',None)
		fire.put('/','temp',item)
		return