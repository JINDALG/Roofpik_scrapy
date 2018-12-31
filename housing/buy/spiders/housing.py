import scrapy
from buy.items import BuyItem
import start_url_housing
from pprint import pprint
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy.http import TextResponse
from scrapy import signals
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from month import find_month
from selenium.webdriver.common.action_chains import ActionChains


class housing(scrapy.Spider):
	name = "housing"
	allowed_domains = ['www.housing.com']

	def __init__(self, filename=None):
		self.driver = webdriver.Chrome()
		dispatcher.connect(self.spider_closed, signals.spider_closed)

	def spider_closed(self,spider):
		self.driver.close()

	def start_requests(self):
		urls = start_url_housing.start()
		for url in urls:
			yield scrapy.Request(url, self.parse)

	def parse(self, response):
		self.driver.get(response.url)
		try:
			WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[@class="list-name"]')))
		except TimeoutException:
			return
		resp = TextResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
		urls = resp.xpath('//a[@class="list-name"]/@href').extract()
		old = 0
		new = len(urls)
		while old != new:
			print "\n\n\n",old,new,"\n\n\n"
			for i in xrange(old,new):
				abs_url = 'http://www.housing.com' + urls[i]
				yield scrapy.Request(abs_url, callback=self.parse_property_info)
			try :
				link = self.driver.find_element_by_xpath('//div[@class="show-more-container"]')
				actions = ActionChains(self.driver)
				actions.click(link)
				actions.perform()
			except:
				self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(3)
			resp = TextResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
			urls = resp.xpath('//a[@class="list-name"]/@href').extract()
			old = new
			new = len(urls)

	def parse_property_info(self, response):
		item = BuyItem()
		
		is_resale = price = bedrooms = bathrooms = price_per_sqft = 0
		is_price_fix = 1
		try :
			price = 0
			price = int(''.join(response.xpath('//span[@class="price-info"]/@data-value').extract()))
		except :
			is_price_fixed = 0

		try :
			price_per_sqft = (''.join(response.xpath('//div[@class="pp-container"]/span/text()').extract()).split())[0]
			price_per_sqft = price_per_sqft.replace(',','')
			price_per_sqft = int(price_per_sqft)
		except :
			pass


		city  = address = location = ""
		try :
			address = (''.join(response.xpath('//div[@class="location-info"]//text()').extract())).replace('\n','')
			city = address.split(',')[-1]
			location = ''.join(response.xpath('//a[@data-category="search"]/span/text()').extract()[5])		
		except :
			pass

		status =  ""
		min_area = max_area = 0.0
		try :
			info_container = response.xpath('//div[@class="project-info-container"]/div')
			for info in info_container:
				try :
					info_description = ''.join(info.xpath('div[@class="info-description"]//text()').extract())
					temp = ''.join(info.xpath('div[@class="info-value"]//text()').extract())
					if "Possession" in info_description :
						status = temp.replace('\n','')

					if ("Sizes" in info_description) or ("area" in info_description):
						temp = temp.split()
						temp = [float(i) for i in temp if i.isdigit()]
						try :
							min_area = temp[0]
							max_area = temp[1]
						except :
							max_area = min_area
				except :
					pass
		except :
			pass


		launch_date = CarpetArea  = posted_on = '' 
		SuperBuiltupArea = 0.0
		try :
			overview = response.xpath('//div[@id="overview-card"]//span[@class="entity"]')
			try :
				for over in overview :
					label = ''.join(over.xpath('span/span[@class="text"]//text()').extract())
					temp = ''.join(over.xpath('span/span[@class="value"]//text()').extract())
					try :
						if "Area" in label :
							SuperBuiltupArea = float((temp.split())[0])
							if "Acres" in temp:
								SuperBuiltupArea = SuperBuiltupArea*43560

					except :
						pass

					try :
						if "Launch" in label:
							launch_date = ((temp.strip().replace('\n','')).replace(',','')).split()
							launch_date[0] = find_month(launch_date[0])
							launch_date = ' '.join(launch_date)
							
					except :
						pass
			except :
				pass
		except :
			pass


		Description =amenities  = age_of_property = ''
		speciality = {}

		try :
			Description = ''.join(response.xpath('//p[@class="desc-para"]//text()').extract())
		except:
			pass
		
		try :
			amenities  = ','.join(response.xpath('//span[@class="amenity-entity"]//span[@class="text"]//text()').extract())
		except:
			pass

		try :
			special  = response.xpath('//div[@class="amenity-entity"]')
			for spec in special :
				try :
					header = ''.join(special.xpath('span[@class="header"]//text()').extract())
					text = ''.join(special.xpath('span[@class="texts"]//text()').extract())
					speciality[header] = text
				except:
					pass

		except :
			pass


		agent_name = agent_type =""
		try :
			agent_name = ''.join(response.xpath('//*[@class="name"]//text()').extract())
			agent_type = ''.join(response.xpath('//div[@class="info"]/div[@class="type"]//text()').extract())
		except :
			pass

		more_info = []
		try :
			information = response.xpath('//div[@class="nsv-list-item-container"]/div')
			bhk = 0
			for info in information :
				try :
					header = ''.join(info.xpath('//text()').extract())
					if "BHK" in header:
						bhk = int(''.join(info.xpath('span/span//text()').extract()).split())[0]
					else :
						size = rate = ""
						size = float(''.join(info.xpath('div/div[@class="list-heading"]//text()').extract()).split())[0]
						full_rate = ''.join(info.xpath('div/div[@class="list-price"]//span/text()').extract())
						rate = float(full_rate.split())[0]
						if 'Lacs' in full_rate:
							rate *= 100000
						if "Cr" in full_rate:
							rate *= 10000000

						more_info += [(bhk,size,rate)]
				except:
					pass
		except :
			pass


		if "resale" in response.url :
			is_resale = 1
			try :
				location = address.split(',')[-2]
			except:
				pass

			try :
				price_per_sqft = (''.join(response.xpath('//div[@class="emi-sub-container"]/span/text()').extract()).split())[0]
				price_per_sqft = price_per_sqft.replace(',','')
				price_per_sqft = int(price_per_sqft)
			except :
				pass
			try :
				overview = response.xpath('//div[@id="overview-card"]//span[@class="entity"]')
				try :
					for over in overview :
						label = ''.join(over.xpath('span/span[@class="text"]//text()').extract())
						temp = ''.join(over.xpath('span/span[@class="value"]//text()').extract())
						
						try :
							if "Price" in label :
								if "negotiable" in temp :
									is_price_fix = 0
						except :
							pass

						try :
							if "Added" in label:
								launch_date = ((temp.replace('\n','')).replace(',','')).split()
								t1 = launch_date[0]
								launch_date[0] = ''
								for i in t1:
									if i.isdigit():
										launch_date[0] += i
								launch_date[1] = find_month(launch_date[1])
								launch_date = ' '.join(launch_date)

								
						except :
							pass

						try :
							if "Bedrooms" in label:
								bedrooms = int(temp.split()[0])
						except :
							pass

						try :
							if "Bathrooms" in label:
								bathrooms = int(temp.split()[0])
						except :
							pass
				except :
					pass
			except :
				pass

			try :
				info_container = response.xpath('//div[@class="project-info-container"]/div')
				for info in info_container:
					try :
						info_description = ''.join(info.xpath('div[@class="info-description"]//text()').extract())
						temp = ''.join(info.xpath('div[@class="info-value"]//text()').extract())
						if "Age of property" in info_description :
							age_of_property = temp.replace('\n','')

					except :
						pass
			except :
				pass


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
