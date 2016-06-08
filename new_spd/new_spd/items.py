# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#http://www.99acres.com/search/property/buy/commercial-all/noida?search_type= scrapy.Field()QS&search_location= scrapy.Field()HP&lstAcn= scrapy.Field()HP_C&src= scrapy.Field()CLUSTER&preference= scrapy.Field()S&selected_tab= scrapy.Field()5&city= scrapy.Field()7&res_com= scrapy.Field()C&property_type= scrapy.Field()C&isvoicesearch= scrapy.Field()N&keyword_suggest= scrapy.Field()noida%3B&area_unit= scrapy.Field()1&fullSelectedSuggestions= scrapy.Field()noida&strEntityMap= scrapy.Field()W3sidHlwZSI6ImNpdHkifSx7IjEiOlsibm9pZGEiLCJDSVRZXzcsIFBSRUZFUkVOQ0VfUywgUkVTQ09NX0MiXX1d&texttypedtillsuggestion= scrapy.Field()noida&refine_results= scrapy.Field()Y&Refine_Localities= scrapy.Field()Refine%20Localities&action= scrapy.Field()%2Fdo%2Fquicksearch%2Fsearch&suggestion= scrapy.Field()CITY_7%2C%20PREFERENCE_S%2C%20RESCOM_C&searchform= scrapy.Field()1&price_min= scrapy.Field()2500000
#http://www.magicbricks.com/property-for-sale/residential-real-estate?proptype= scrapy.Field()Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment&cityName= scrapy.Field()Gurgaon&BudgetMin= scrapy.Field()40-Lacs

class NewSpdItem(scrapy.Item):
	# define the fields for your item here like:
	
	Price = scrapy.Field()   
	PricePerUnit = scrapy.Field() 
	Availability = scrapy.Field() 
	SuperBuiltupArea = scrapy.Field()
	BuiltupArea = scrapy.Field()
	CarpetArea = scrapy.Field()
	
	city = scrapy.Field()
	address = scrapy.Field() 
	Location = scrapy.Field() 
	Washroom = scrapy.Field()
	Description = scrapy.Field() 

	PostedBy = scrapy.Field() 
	PostingDate = scrapy.Field() 
	ProjectName = scrapy.Field() 
	Bedrooms = scrapy.Field() 
	Views = scrapy.Field()
	Searched = scrapy.Field()
	URL = scrapy.Field()
	Question = scrapy.Field() 
	Trends = scrapy.Field()
	PROPERTYCODE = scrapy.Field() 
	BookingAmount = scrapy.Field()
	Deposit = scrapy.Field() 
	GatedCommunity = scrapy.Field() 
	PowerBackup = scrapy.Field() 
	BookingINFO = scrapy.Field() 
	AdditionalRooms = scrapy.Field() 
	PropertyInfo = scrapy.Field() 
	maintainance = scrapy.Field()
	Furnishing = scrapy.Field()
