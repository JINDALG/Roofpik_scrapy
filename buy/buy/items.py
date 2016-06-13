# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BuyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    price = scrapy.Field()
    price_per_sqft = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
    locaiton = scrapy.Field()
    build_up_area = scrapy.Field()
    carpet_area = scrapy.Field()
    age_of_property = scrapy.Field()
    is_price_fixed = scrapy.Field()
   	launched_date = scrapy.Field()
   	status = scrapy.Field()
   	agent = scrapy.Field()
   	amenities = scrapy.Field()
   	speciality = scrapy.Field()
   	more_info = scrapy.Field()
    pass
