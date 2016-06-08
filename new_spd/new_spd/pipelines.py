# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from new_spd.DBHandler import DBHandler 
from new_spd.DBCreater import create_db 

class NewSpdPipeline(object):
	def __init__(self):
		self.dbh = DBHandler()

	def process_item(self, item, spider):
		# check thoroughly
		print '\n\n\n\n\n\n', item['Question'] ,'\n\n\n\n\n\n' , item['Trends']

		self.dbh.insert_into_questions(item['Question'])
		self.dbh.insert_into_trends(item['Trends'])

		self.dbh.insert_into_db(  item['Price'], item['PricePerUnit'], 
        	item['Availability'], item['SuperBuiltupArea'], item['BuiltupArea'], 
        	item['CarpetArea'], item['address'], item['Location'], 
        	item['Washroom'], item['Description'], item['PostedBy'], 
        	item['PostingDate'], item['ProjectName'], item['Bedrooms'], 
        	item['Views'], item['Searched'], item['URL'], 
        	item['PROPERTYCODE'], item['BookingAmount'], item['Deposit'], 
        	item['GatedCommunity'], item['PowerBackup'], item['BookingINFO'],
        	item['AdditionalRooms'], item['PropertyInfo'], item['maintainance'],
        	item['Furnishing'], item['city'] )