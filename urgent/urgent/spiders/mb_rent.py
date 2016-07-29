import scrapy
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
import json
import os

from pyvirtualdisplay import Display
	
class magicbricks(scrapy.Spider):
	name = "magic"
	allowed_domains = ['www.magicbricks.com']
	start_urls = ['http://www.magicbricks.com/property-for-rent/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Service-Apartment,Residential-House,Villa&cityName=Gurgaon&projectSocity=vipul%20green']
	def __init__(self,filename=None):
		with open(os.path.dirname(__file__) + '/../../link.txt','r') as f:
			self.start_urls = [f.read()]
		self.obj = {}
		self.display = Display(visible=0, size=(800, 600))
		self.display.start()
		self.driver = webdriver.Chrome()
		dispatcher.connect(self.spider_closed, signals.spider_closed)
		with open('cus.txt','ab+') as f:
			f.write("init complete")

	def spider_closed(self,spider):
		self.driver.close()
		self.display.stop()
		

	def parse(self, response):
		try :
			with open('cus.txt','ab+') as f:
				f.write("parse enter")			
			self.driver.get(response.url)
			with open('cus.txt','ab+') as f:
				f.write("url load")
			resp = TextResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
			blocks = resp.xpath('//div[contains(@id,"resultBlockWrapper")]')
			old = 0
			new = len(blocks)
			while old != new:
				print "\n\n\n",old,new,"\n\n\n"
				self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(3)
				resp = TextResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
				blocks = resp.xpath('//div[contains(@id,"resultBlockWrapper")]')
				old = new
				new = len(blocks)
			with open('cus.txt','ab+') as f:
				f.write("scrolling complete")
			for block in blocks:
				try :
					price = ''.join(block.xpath('div//div[@class="srpColm2"]//span[contains(@id,"pricePropertyVal")]//text()').extract())
					iscr = 'Cr' in price
					islac = 'Lac' in price
					price = price.replace(',','').replace('Cr','').replace('Lac','')
					price = float(price.split()[0])	
					price *= 10000000 if iscr else 1
					price *= 100000 if islac else 1
					bhk = ''.join(block.xpath('div//div[@class="srpColm2"]//strong/text()').extract())
					bhk = (''.join(bhk.split()[:2])).replace('.5','')
					if "bhk" in bhk.lower():
						ppf = ''.join(block.xpath('div//div[@class="srpColm2"]//span[@class="proRentArea"]/text()').extract())
						if ppf == "":
							ppf = ''.join(block.xpath('div//div[@class="srpColm2"]//span[@class="proNameSizeTxt"]/text()').extract())
						ppf = float(ppf.split()[0])
						if bhk in self.obj:
							self.obj[bhk]['min'] = self.obj[bhk]['min'] if price > self.obj[bhk]['min'] else price
							self.obj[bhk]['max'] = self.obj[bhk]['max'] if price < self.obj[bhk]['max'] else price
							self.obj[bhk]['count'] += 1
							self.obj[bhk]['avg'] += ppf
						else :
							self.obj[bhk] = {'min':price, 'max':price, 'count':1,'avg':ppf}
				except :
					pass
			with open('cus.txt','ab+') as f:
				f.write("data mined")
			with open(os.path.dirname(__file__) +'/../../price.json','w')as file:
				file.write(json.dumps(self.obj))
			with open('cus.txt','ab+') as f:
				f.write("data wrote in file")
			return
		except :
			with open('cus.txt','ab+') as f:
				f.write("some error occur")
			return	