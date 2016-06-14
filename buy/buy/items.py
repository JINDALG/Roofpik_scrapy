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
    is_price_fix = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
    location = scrapy.Field()
    min_area = scrapy.Field()
    max_area = scrapy.Field()
    SuperBuiltupArea = scrapy.Field()
    age_of_property = scrapy.Field()
    launch_date = scrapy.Field()
    possession_status = scrapy.Field()
    agent_name = scrapy.Field()
    agent_type = scrapy.Field()
    amenities = scrapy.Field()
    speciality = scrapy.Field()
    more_info = scrapy.Field()
    url = scrapy.Field()
    bedrooms = scrapy.Field()
    bathrooms = scrapy.Field()
    is_resale = scrapy.Field()    	