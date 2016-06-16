import os
import scrapy
from selenium.webdriver.common.action_chains import ActionChains
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.http import TextResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from Tkinter import *
from pprint import pprint
import csv


class Result(scrapy.Spider):
    name = "trends"
    text = None
    allowed_domains = ['google.co.in']
    start_urls = ['https://www.google.co.in']

    def fetch(self,entries):
        sroll = entries[0]
        self.text = '+'.join((entries[0][1].get()).split())
        self.root.destroy()

    def makeform(self,fields):
       entries = []
       for field in fields:
          row = Frame(self.root)
          lab = Label(row, width=15, text=field, anchor='w')
          ent = Entry(row)
          row.pack(side=TOP, fill=X, padx=5, pady=10)
          lab.pack(side=TOP)
          ent.pack(side=TOP, expand=YES, fill=X , pady=10)
          entries.append((field, ent))
       return entries

    def __init__(self, filename=None):
        with open('data.csv','wb') as csvfile:
            fieldnames = ['url','p','a','span','h1','h2','h3','h4','h5','h6','title','meta','li','img','th','td']
            writer = csv.DictWriter(csvfile, fieldnames)
            writer.writeheader()
        fields = 'Googling Text',
        self.root = Tk()
        self.root.title('Roofpik')
        self.root.geometry("200x200")
        ents = self.makeform( fields)
        self.root.bind('<Return>', (lambda event, e=ents: self.fetch(e)))   
        b1 = Button(self.root, text='submit',
                command=(lambda e=ents: self.fetch(e)))
        b1.pack(side=TOP, padx=5, pady=5)
        self.root.mainloop()
        self.driver = webdriver.Chrome()
        # self.driver = webdriver.Firefox()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        self.driver.close()


    def parse(self, response):
        
        self.driver.get('https://www.google.co.in/?gfe_rd=cr&ei=cUFiV5C4Lu-q8weqqI-oAQ&gws_rd=ssl#q=%s' %(self.text))
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//h3//a')))
        except TimeoutException:
            return
        resp = TextResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8');

        urls = resp.xpath('//h3//a/@href').extract()
        for url in urls :
            yield scrapy.Request(url, callback = self.parse_page)



    def parse_page(self, response):
        self.driver.get(response.url)
        temp = {}
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//img[@src]')))
        except TimeoutException:
            pass
        resp = TextResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8');
        temp['p'] = resp.xpath('//p//text()').extract()
        temp['a'] = resp.xpath('//a//text()').extract()
        temp['span'] = resp.xpath('//span//text()').extract()
        temp['h1'] = resp.xpath('//h1//text()').extract()
        temp['h2'] = resp.xpath('//h2//text()').extract()
        temp['h3'] = resp.xpath('//h3//text()').extract()
        temp['h4'] = resp.xpath('//h4//text()').extract()
        temp['h5'] = resp.xpath('//h5//text()').extract()
        temp['h6'] = resp.xpath('//h6//text()').extract()
        temp['title'] = resp.xpath('//title//text()').extract()
        temp['meta'] = resp.xpath('//meta//text()').extract()
        temp['li'] = resp.xpath('//li//text()').extract()
        temp['img'] = resp.xpath('//img/@alt').extract()
        temp['th'] = resp.xpath('//th//text()').extract()
        temp['td'] = resp.xpath('//td//text()').extract() 
        temp['url'] = response.url

        with open('data.csv','ab') as csvfile:
            fieldnames = ['url','p','a','span','h1','h2','h3','h4','h5','h6','title','meta','li','img','th','td']
            writer = csv.DictWriter(csvfile, fieldnames)
            writer.writerow(temp)

        pprint(temp)

        yield temp

        
        


