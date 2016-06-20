# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class SquareyardItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    min_price = scrapy.Field()
    max_price = scrapy.Field()
    price_per_sqft = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
    location = scrapy.Field()
    min_area = scrapy.Field()
    max_area = scrapy.Field()	
    possession_status = scrapy.Field()
    amenities = scrapy.Field()
    speciality = scrapy.Field()
    url = scrapy.Field()
    is_resale = scrapy.Field()  
    code = scrapy.Field()  	
    description = scrapy.Field()
    unit_type = scrapy.Field()
    property_type = scrapy.Field()
    wow_factors = scrapy.Field()
    connecting_road = scrapy.Field()
    index = scrapy.Field()
    more_info = scrapy.Field()
    pass
