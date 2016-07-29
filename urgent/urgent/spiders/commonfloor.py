#!usr/bin/python -tt
import scrapy 
import json
from pprint import pprint
import re
import os
import time
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy.http import TextResponse
from scrapy import signals
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from pyvirtualdisplay import Display

class commonfl(scrapy.Spider):
	name = "common"
	allowed_domains = ["commonfloor.com"]   # target site
	start_urls = ['https://www.commonfloor.com/listing-search?city=Gurgaon&prop_name%5B%5D=DLF+Park+Place+-+Park+Heights&property_location_filter%5B%5D=apartment_hfmxpv&use_pp=0&set_pp=1&polygon=1&page=1&page_size=30&search_intent=rent&min_inr=&max_inr=']
	def __init__(self, filename=None):
		with open(os.path.dirname(__file__) + '/../../link.txt','r') as f:
			self.start_urls = [f.read()]
		self.obj = {}
		self.display = Display(visible=0, size=(800, 600))
		self.display.start()
		self.driver = webdriver.Chrome()
		dispatcher.connect(self.spider_closed, signals.spider_closed)

	def spider_closed(self, spider):
		self.driver.close()
		self.display.stop()

	def parse(self, response):
		self.driver.get(response.url)
		try:
			WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="row listing"]')))
		except TimeoutException:
			return
		resp = TextResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
		block = resp.xpath('//div[@class="row listing"]')
		for box in block:
			try :
				price = ''.join(box.xpath('div[2]/div[2]/div/div[1]/div[2]/p/span[2]/text()').extract())
				iscr = 'Cr' in price
				islac = 'L' in price
				price = price.replace(',','').replace('Cr','').replace('L','')
				price = float(price.encode('utf8'))
				price *= 10000000 if iscr else 1
				price *= 100000 if islac else 1
				bhk = ''.join(box.xpath('div[2]/div[1]/div/div/h4/a/span[1]/text()').extract())
				bhk = bhk.split()[0].replace('.5','')
				if "bhk" in bhk.lower():
					ppf = ''.join(box.xpath('div[2]/div[2]/div/div[2]/div[2]/p/text()').extract())
					ppf = float(ppf)
					ppf = price/ppf
					if bhk in self.obj:
						self.obj[bhk]['min'] = self.obj[bhk]['min'] if price > self.obj[bhk]['min'] else price
						self.obj[bhk]['max'] = self.obj[bhk]['max'] if price < self.obj[bhk]['max'] else price
						self.obj[bhk]['count'] += 1
						self.obj[bhk]['avg'] += ppf
					else :
						self.obj[bhk] = {'min':price, 'max':price, 'count':1,'avg':ppf}
			except :
				pass

		while 1:
			next_button = self.driver.find_element_by_xpath('//span[@class="icon-navigate_next"]')
			check = resp.xpath('//ul[@class="pagination pageNumber"]/li/@style').extract()[-1]
			if "none" in check:
				print self.obj
				with open(os.path.dirname(__file__) +'/../../price.json','w')as file:
					file.write(json.dumps(self.obj))
				return
			actions = ActionChains(self.driver)
			actions.click(next_button)
			actions.perform()
			time.sleep(2)
			resp = TextResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
			block = resp.xpath('//div[@class="row listing"]')
			for box in block:
				try :
					price = ''.join(box.xpath('div[2]/div[2]/div/div[1]/div[2]/p/span[2]/text()').extract())
					iscr = 'Cr' in price
					islac = 'L' in price
					price = price.replace(',','').replace('Cr','').replace('L','')
					price = float(price.encode('utf8'))
					price *= 10000000 if iscr else 1
					price *= 100000 if islac else 1
					bhk = ''.join(box.xpath('div[2]/div[1]/div/div/h4/a/span[1]/text()').extract())
					bhk = bhk.split()[0].replace('.5','')
					if "bhk" in bhk.lower():
						ppf = ''.join(box.xpath('div[2]/div[2]/div/div[2]/div[2]/p/text()').extract())
						ppf = float(ppf)
						ppf = price/ppf
						if bhk in self.obj:
							self.obj[bhk]['min'] = self.obj[bhk]['min'] if price > self.obj[bhk]['min'] else price
							self.obj[bhk]['max'] = self.obj[bhk]['max'] if price < self.obj[bhk]['max'] else price
							self.obj[bhk]['count'] += 1
							self.obj[bhk]['avg'] += ppf
						else :
							self.obj[bhk] = {'min':price, 'max':price, 'count':1,'avg':ppf}
				except :
					pass

		return 