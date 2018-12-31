import scrapy
from buy.items import BuyItem
import start_url_acres
from pprint import pprint
from month import find_month
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy.http import TextResponse
from scrapy import signals
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver.common.action_chains import ActionChains

class acres(scrapy.Spider):
	name = "acres"
	allowed_domains = ['www.99acres.com']

	def __init__(self, filename=None):
		self.driver = webdriver.Chrome()
		dispatcher.connect(self.spider_closed, signals.spider_closed)

	def spider_closed(self,spider):
		self.driver.close()

	def start_requests(self):
		urls = start_url_acres.start()
		for url in urls:
			yield scrapy.Request(url, self.parse)

	def parse(self, response):
		urls = response.xpath('//div[@class="wrapttl"]/div/a/@href').extract()
		if len(urls) == 0:
			return
		for url in urls:
			abs_url = 'http://www.99acres.com' + url
			yield scrapy.Request(abs_url, callback=self.parse_property_info)
		next_url = 'http://www.99acres.com' + response.xpath('//div[@class="pgdiv"]//a/@href').extract()[-1]
		yield scrapy.Request(next_url, callback=self.parse)


	def parse_property_info(self, response):
		item = BuyItem()
		self.driver.get(response.url)
		input()
		try:
			WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="npPrice"]//text()')))
		except TimeoutException:
			return
		response = TextResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
		is_resale = price = bedrooms = bathrooms = price_per_sqft = 0
		is_price_fix = 1
		print "\n",response.url,"\n"
		try :
			full_price = ','.join(response.xpath('//div[@class="npPrice"]//text()').extract())
			print full_price
			print price
			price = float(full_price.split(',')[3])
			if 'Cr' in full_price :
				price *= 10000000
			if "Lac" in full_price :
				price *= 100000
		except :
			pass

		if price == 0:
			try :
				full_price = ' '.join(response.xpath('//span[@id="pdPrice"]//text()').extract())
				print full_price
				print price
				price = float(full_price.split()[0])
				if 'Cr' in full_price :
					price *= 10000000
				if "Lacs" in full_price :
					price *= 100000
			except :
				pass
		print price
		input()

		try :
			price_per_sqft = float((response.xpath('//div[@class="npBasePrice"]/span/text()').extract())[3])
		except :
			pass

		try :
			price_per_sqft = float((response.xpath('//div[@id="pricePerUnitArea"]/text()').extract()).split()[1])
		except :
			pass


		city  = address = location = ""
		try :
			address = (''.join(response.xpath('//div[@class="project-location"]/span//text()').extract())).replace('\n','')
			city = address.split(',')[-2]
			location = (response.xpath('//a[@class="ttlLink"]/text()').extract()[1])		
		except :
			pass

		if address == "":
			try :
				address = (''.join(response.xpath('//span[@id="address"]/text()').extract())).replace('\n','')
				city = address.split(',')[-2]
				location = (response.xpath('//a[@class="ttlLink"]/text()').extract()[1])	
			except :
				pass

		status =  ""
		min_area = max_area = 0.0
		try :
			status = ''.join(response.xpath('//div[@class="npPossessionDate"]/text()').extract()[2])	
		except:
			pass

		if status == "":
			try :
				status = ''.join(response.xpath('//div[@class="pdDetailInfoOther"]/div[3]/span/text()').extract())	
			except:
				pass
		try :
			temp = ''.join(response.xpath('//div[@class="npAreaPrice"]/span[1]/text()').extract())
			temp = temp.split()
			temp = [float(i) for i in temp if i.isdigit()]
			try :
				min_area = temp[0]
				max_area = temp[1]
			except :
				max_area = min_area
		except :
			pass

		SuperBuiltupArea = 0.0
		try :
			SuperBuiltupArea = ' '.join(response.xpath('//div[@class="npPrjArea"]	/span//text()').extract())
			if "acres" in SuperBuiltupArea:
				SuperBuiltupArea = float(SuperBuiltupArea.split()[0])*43560
			else :
				SuperBuiltupArea = float(SuperBuiltupArea.split()[0])
		except :
			pass


		if min_area == 0.0 :
			try :
				min_area = float(''.join(response.xpath('//span[@id="superbuiltupArea_span"]/text()').extract()))
				max_area = min_area

			except :
				pass

			try :
				SuperBuiltupArea = ''.join(response.xpath('//div[@id="socAreaOccupied"]/text()').extract())
				if "acres" in SuperBuiltupArea:
					SuperBuiltupArea = float(SuperBuiltupArea.split()[0])*43560
				else :
					SuperBuiltupArea = float(SuperBuiltupArea.split()[0])	
			except:
				pass


		launch_date = CarpetArea = posted_on = ''

		try :
			posted_on = (''.join(response.xpath('//span[@class="pdPropDate"]/text()').extract()).replace(',','')).split()
			posted_on[0],posted_on[1] = posted_on[1],posted_on[0]
			posted_on[1] =  find_month(posted_on[1])
			posted_on = ' '.join(posted_on)

		except :
			pass



		Description =amenities  = age_of_property = ''
		speciality = {}

		try :
			Description = (''.join(response.xpath('//div[@id = "description"]//text()').extract())).replace('\n','')
		except:
			pass
		
		try :
			amenities  = ','.join(response.xpath('//div[@id="amenitiesSection"]/div/div[2]/div/div/div//text()').extract())
		except:
			pass

		if amenities == "":
			try :
				amenities  = ','.join(response.xpath('//div[@id="features"]/div/div//text()').extract())
			except:
				pass

		try :
			special  = response.xpath('//div[@class=" pdOtherFacts responsive"]/div')
			for spec in special :
				try :
					header = ''.join(special.xpath('span[1]//text()').extract())
					text = ''.join(special.xpath('span[2]//text()').extract())
					speciality[header] = text
				except:
					pass

		except :
			pass



		agent_name = agent_type =""
		try :
			agent_type = ''.join(response.xpath('//div[@id="QryFormPd"]//span[@class="dealerWidgetHeading"]//text()').extract())
			agent_type = agent_type.replace('Details','')
			agent_name = (','.join(response.xpath('//div[@id="QryFormPd"]//div[@class="c2dInfo"]//text()').extract())).split()[0]
		except :
			pass

		if agent_name == "" :
			try :
				agent_name = (' '.join(response.xpath('//div[@id="QryFormPd"]//div[@class="c2dRunCaptionAbtDev "]//span[@class="spanBold"]//text()').extract()))
				agent_name = agent_name.replace('About ','')
			except :
				pass

		try :
			resale = response.xpath('//span[@id="transactionType"]//text()').extract()
			if 'Resale' in resale:
				is_resale = 1
		except:
			pass

		try :
			bedrooms = int((''.join(response.xpath('//div[@id="bedRoomNum"]//text()').extract())).split()[0])
		except :
			pass

		try :
			bathrooms = int((''.join(response.xpath('//div[@id="bathroomNum"]//text()').extract())).split()[0])
		except :
			pass

		try :
			age_of_property = ''.join(response.xpath('//div[@id="agePossessionLbl"]//text()').extract())
		except :
			pass

		try :
			additional_rooms = ''.join(response.xpath('//div[@id="additionalRooms"]//text()').extract())
			amenities += (", " + additional_rooms)	
		except :
			pass

		more_info = {}

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

		yield item
		input()