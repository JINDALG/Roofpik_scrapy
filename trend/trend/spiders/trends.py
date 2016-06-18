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
import urlparse


class Result(scrapy.Spider):
    name = "trends"
    text = None
    allowed_domains = ['google.co.in']
    start_urls = ['https://www.google.co.in']
    page = 0

    def fetch(self,entries):
        sroll = entries[0]
        self.text = '+'.join((entries[0][1].get()).split())
        self.root.destroy()

    def makeform(self,fields):
       entries = []
       for field in fields:
          row = Frame(self.root)
          lab = Label(row, width=50, text=field, anchor='w')
          ent = Entry(row)
          row.pack(side=TOP, fill=X, padx=5, pady=10)
          lab.pack(side=TOP)
          ent.pack(side=TOP, expand=YES, fill=X , pady=10)
          entries.append((field, ent))
       return entries

    def __init__(self, filename=None):
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
        url = 'https://www.google.co.in/?gfe_rd=cr&ei=cUFiV5C4Lu-q8weqqI-oAQ&gws_rd=ssl#q=%s&start=%d' %(self.text,self.page)
        self.driver.get(url)
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//h3//a')))
        except TimeoutException:
            return
        resp = TextResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8');
        urls = resp.xpath('//h3//a/@href').extract()
        for url in urls :
            try :
                yield scrapy.Request(url,callback = self.parse_page, dont_filter = True)
            except:
                pass
        self.page += 10
        if self.page != 60:
            next_url = (resp.xpath('//tr[@valign="top"]/td/a/@href').extract())[-1]
            next_url = urlparse.urljoin(self.start_urls[0],next_url)
            yield scrapy.Request(next_url, callback = self.parse, dont_filter = True)

    def filter(self, url):
        banned = ['magicbricks.com','99acres.com','commonfloor.com','www.makaan.com','']
        parsed_uri = urlparse.urlparse(url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        print domain
        if str(domain) in banned:
            return False
        return True

    def parse_page(self, response):
        if self.filter(response.url):
            temp = {}
            self.driver.get(response.url)
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//img[@src]')))
            except TimeoutException:
                yield scrapy.Request(response.url, callback = self.parse_page)
                return
            resp = TextResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8');
            temp['p'] = ((('abcd'.join(resp.xpath('//p//text()').extract())).replace('\n','').replace('\t','')).encode('utf8')).split('abcd')
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

            for item in temp:
                try :
                    temp[item] = (('abcd'.join(temp[item])).replace('\n','').replace('\t','').replace(',',' '))
                    temp[item] = re.sub(' +',' ',temp[item])
                    temp[item] = (''.join([i if ord(i) < 128 else '' for i in temp[item]])).encode('utf8').split('abcd')

                except :
                    pass
            temp['url'] = response.url

            with open('query_data.csv','ab+') as csvfile:
                fieldnames = ['url','p','a','span','h1','h2','h3','h4','h5','h6','title','meta','li','img','th','td']
                writer = csv.DictWriter(csvfile, fieldnames)
                reader = csv.DictReader(csvfile)
                writer.writerow(temp)

            yield temp

        
        


