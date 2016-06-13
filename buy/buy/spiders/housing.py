import scrapy
from new_spd.items import NewSpdItem
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
from selenium.webdriver.common.action_chains import ActionChains


class housing(scrapy.Spider):
	name = "housing"
	allowed_domains = ['housing.com']

	def __init__(self, filename=None):
		self.driver = webdriver.Firefox()
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
			print "time out"
			input()
		old = 1
		new = 21
		resp = TextResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
		urls = resp.xpath('//a[@class="list-name"]/@href').extract()
		while old != new:
			print "\n\n\n",old,new,"\n\n\n"
			for i in xrange(old,new):
            	abs_url = 'http://www.housing.com' + urls[i]
            	yield scrapy.Request(abs_url, callback=self.parse_property_info)
   			try:
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
			new = len(urls)+1

	def parse_property_info(self, response):
		item = NewSpdItem()	
		
		try :
			price = 0
			price = (''.join(response.xpath('//span[@class="price-info"]/@data-value').extract()).spilit())[0]
		except :
			pass

		try :
			PricePerUnit = 0
			PricePerUnit = (''.join(response.xpath('//div[@class="pp-container"]/span/text()').extract()).spilit())[0]
			PricePerUnit = PricePerUnit.replace(',','')
			PricePerUnit = int(PricePerUnit)
		except :
			pass

		if PricePerUnit = 0:
			try :
				PricePerUnit = 0
				PricePerUnit = (''.join(response.xpath('//div[@class="emi-sub-container"]/span/text()').extract()).spilit())[0]
				PricePerUnit = PricePerUnit.replace(',','')
				PricePerUnit = int(PricePerUnit)
			except :
				pass

		Availability = '' ## availability not available on housing.com
		status = ""
		BuiltupArea = 0
		try :
			info_container = response.xpath('//div[@class="project-info-container"]/div')
			for info in info_container:
				try :
					info_description = ''.join(info.xpath('div[@class="info-description"]//text()').extract())
					temp = ''.join(info.xpath('div[@class="info-value"]//text()').extract())
					if "Possession" in info-description :
						status = temp

					if "Sizes" in info-description or "area" in info-description:
						BuiltupArea = int((temp[0].spilit())[0])
				except :
					pass
		except :
			pass

		SuperBuiltupArea = launch_date = CarpetArea = '' 
		try :
			overview = response.xpath('//div[@id="overview-card"]//span[@class="entity"]')
			try :
				for over in overview :
					label = ''.join(over.xpath('span/span[@class="text"]//text()').extract())
					temp = ''.join(over.xpath('span/span[@class="value"]//text()').extract())
					try :
						if "AREA" in label :
							SuperBuiltupArea = temp
					except :
						pass

					try :
						if "LAUNCH" in label:
							launch_date = temp
					except :
						pass
			except :
				pass
		except :
			pass


		city  = address = Location = Description =aminity = ''
		speciality = {}

		try :
			address = ''.join(response.xpath('//div[@class="location-info"]//text()').extract())
			city = (address.spilit(','))[-1]
		except :
			pass

		try :
			Description = ''.join(response.xpath('//p[@class="desc-para"]//text()').extract())
		except:
			pass

		
		try :
			aminity  = ' '.join(response.xpath('//span[@class="amenity-entity"]//span[@class="text"]//text()').extract())
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





