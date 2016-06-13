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
		
			