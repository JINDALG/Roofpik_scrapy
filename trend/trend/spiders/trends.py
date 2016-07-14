import os
import scrapy
from pprint import pprint
import csv
import re
import datetime
from firebase import firebase
from multiprocessing import Process


class Result(scrapy.Spider):
    name = "trends"
    city = "Mumbai"
    allowed_domains = ['google.co.in']
    start_urls = ['https://www.google.co.in']
    def __init__(self, filename=None):
        self.firebases = firebase.FirebaseApplication("https://trends-4b774.firebaseio.com/", None)
        pass
        # self.driver = webdriver.Chrome()
        # # self.driver = webdriver.Firefox()
        # dispatcher.connect(self.spider_closed, signals.spider_closed)

    # def spider_closed(self, spider):
    #     self.driver.close()


    def parse(self, response):
        query_list = (self.firebases).get('/searchQuery/city', None)
        query_list = query_list.values()
        for query in query_list:
            query = query['name'].encode('utf8')
            text= query %(self.city)
            text = text.replace("?",'').replace('.','')
            yield scrapy.FormRequest.from_response(
                response,
                formdata={'q': text,'start':str(0)},
                callback=self.link_parse
            )
        # url = 'https://www.google.co.in/?gfe_rd=cr&ei=cUFiV5C4Lu-q8weqqI-oAQ&gws_rd=ssl#q=%s&start=%d' %(text,self.page)
        # self.driver.get(url)
        # try:
        #     WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//h3//a')))
        # except TimeoutException:
        #     return
        # resp = TextResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8');
        

        
    def link_parse(self, response):
        page = int((response.url).split('=')[-1])
        page += 10
        text = response.xpath('//input[@name="q"]/@value').extract()
        text = text[0].encode('utf8')
        urls = response.xpath('//h3//a/@href').extract()
        for url in urls :
            try :
                try :
                    rank = page - 10 + urls.index(url)
                except :
                    rank = 0
                rank += 1
                url = url.replace('/url?q=','')
                request =  scrapy.Request(url,callback = self.parse_page, dont_filter = True)
                request.meta['rank'] = rank
                request.meta['text'] = text
                yield request
            except:
                pass
        if page != 60:
            yield scrapy.FormRequest.from_response(
                response,
                formdata={'q': text,'start':str(page)},
                callback=self.link_parse
            )

    def filter(self, url):
        with open('query_data.csv','ab+') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['url'] == url:
                    return False
        return True


    def parse_page(self, response):
        if self.filter(response.url):
            city = self.city
            date = (datetime.date.today()).isoformat()
            rank = int(response.meta['rank'])
            website = (response.url).split('/')[2]
            temp = {}
            date_object = {}

            # self.driver.get(response.url)
            # try:
            #     WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//img[@src]')))
            # except TimeoutException:
            #     yield scrapy.Request(response.url, callback = self.parse_page)
            #     return
            # resp = TextResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8');
            temp['p'] = ((('abcd'.join(response.xpath('//p//text()').extract())).replace('\n','').replace('\t','')).encode('utf8')).split('abcd')
            temp['a'] = response.xpath('//a//text()').extract()
            temp['span'] = response.xpath('//span//text()').extract()
            temp['h1'] = response.xpath('//h1//text()').extract()
            temp['h2'] = response.xpath('//h2//text()').extract()
            temp['h3'] = response.xpath('//h3//text()').extract()
            temp['h4'] = response.xpath('//h4//text()').extract()
            temp['h5'] = response.xpath('//h5//text()').extract()
            temp['h6'] = response.xpath('//h6//text()').extract()
            temp['title'] = response.xpath('//title//text()').extract()
            temp['meta'] = response.xpath('//meta//text()').extract()
            temp['li'] = response.xpath('//li//text()').extract()
            temp['img'] = response.xpath('//img/@alt').extract()
            temp['th'] = response.xpath('//th//text()').extract()
            temp['td'] = response.xpath('//td//text()').extract() 

            for item in temp:
                try :
                    temp[item] = (' '.join(temp[item])).replace('\n','').replace('\t','').replace(',',' ').replace('\r','')
                    temp[item] = re.sub(' +',' ',temp[item])
                    temp[item] = re.sub(r'[^\x00-\x7F]',' ', temp[item])
                    temp[item] = temp[item].encode('utf8')


                except :
                    pass


            date_object['link'] = response.url
            date_object['rank'] = rank
            date_object['website'] = website
            date_object['content'] = temp

            # with open('query_data.csv','ab+') as csvfile:
            #     fieldnames = ['url','p','a','span','h1','h2','h3','h4','h5','h6','title','meta','li','img','th','td']
            #     writer = csv.DictWriter(csvfile, fieldnames)
            #     reader = csv.DictReader(csvfile)
            #     writer.writerow(temp)

            #firebase.get('/users', None)
            pprint(date_object)
            
            print (self.firebases).put("/","SearchURL/city/"+city+"/"+date+"/"+response.meta['text']+"/"+"url"+str(rank),date_object)
            yield temp
        
        


