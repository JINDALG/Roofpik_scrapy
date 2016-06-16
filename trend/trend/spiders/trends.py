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


class Result(scrapy.Spider):
    name = "trends"
    text = None
    allowed_domains = ['google.co.in']
    start_urls = ['https://www.google.co.in/']

    def fetch(self,entries):
        sroll = entries[0]
        self.text =entries[0][1].get()
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
        fields = 'Googing text' ,
        self.root = Tk()
        self.root.title('RoofPik')
        self.root.geometry("200x200")
        ents = self.makeform( fields)
        self.root.bind('<Return>', (lambda event, e=ents: self.fetch(e)))   
        b1 = Button(self.root, text='submit',
                command=(lambda e=ents: self.fetch(e)))
        b1.pack(side=TOP, padx=5, pady=5)
        self.root.mainloop()
        #self.driver = webdriver.Chrome()
        # self.driver = webdriver.Firefox()
        # dispatcher.connect(self.spider_closed, signals.spider_closed)

    # def spider_closed(self, spider):
    #     self.driver.close()


    def parse(self, response):
        # try :
        #     self.driver.get(response.url)
        #     try:
        #         WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="lst-ib"]')))
        #     except TimeoutException:
        #         return
        #     resp = TextResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
        #     entry = self.driver.find_element_by_name('q')
        #     entry.send_keys(self.text)
        #     button = self.driver.find_element_by_name('btnK')
        #     actions = ActionChains(self.driver)
        #     actions.click(button)
        #     actions.perform()
        #     resp = TextResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8');

        # except httplib.BadStatusLine:
        #     print "error"

        return scrapy.FormRequest.from_response(
            response,
            formdata={'q': self.text,},
            callback=self.after_login
        )



    def after_login(self, response):
        # check login succeed before going on
        temp = response.xpath("//div/text()").extract()[1]
        print "\n\n",response.url
        print "\n\n",temp,"\n\n\n"
        print temp
        

