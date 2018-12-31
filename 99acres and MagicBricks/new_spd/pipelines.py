# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from new_spd.DBHandler import DBHandler 
from new_spd.DBCreater import create_db 
import traceback

class NewSpdPipeline(object):
    def __init__(self):
    	self.dbh = DBHandler()

    def process_item(self, item, spider):
        try :
            self.dbh.insert_into_db(item['Price'],item['PricePerUnit'], item['SuperBuiltupArea'], 
                item['CarpetArea'], item['address'], item['Location'], item['Washroom'], item['PostedBy'], 
                item['PostingDate'], item['ProjectName'], item['Bedrooms'], item['URL'], item['maintainance'], 
                item['city'], item['is_price_fixed'], item['website'] )
        except :
            print traceback.print_exc()
            input()