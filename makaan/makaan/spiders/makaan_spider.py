# -*- coding: utf-8 -*-
#usr/bin/python -tt
import scrapy


class MakaanSpiderSpider(scrapy.Spider):
	name = "makaan_spider"
	allowed_domains = ["makaan.com"]
	start_urls = [
        'https://www.makaan.com/gurgaon-residential-property/rent-property-in-gurgaon-city'
	]

	def parse(self, response):
		page_no = 1
		urls = response.xpath('//h2//a/@href').extract() 	
		new_lst = response.xpath('//div[@class="wrapttl"]//text()').extract()   

		if len(urls) == 0: return   # return if no property listed on page i.e end of listing

		print '\n\n\n\n\n\nurls = ', urls , len(urls)

		for url in urls:
			abs_url = 'http://www.makaan.com' + url
			#print '\n\n\n\n\n\n\nhttp://www.makaan.com' + url 
			yield scrapy.Request(abs_url, callback=self.parse_property_info)
            
		next_url = 'https://www.makaan.com/gurgaon-residential-property/rent-property-in-gurgaon-city?page=' + str(page_no)
		#yield scrapy.Request(next_url, callback=self.parse)	

	def parse_property_info(self, response):
		furnishing = availaiblity = ''
		deposit = -1

		try:
			data = response.xpath('//div[@class="sub-points"]//text()').extract()

			for i in range(0, len(data)):
				if(data[i] == 'Availability'):
					availaiblity = data[i-1].encode('utf-8')
				elif(data[i] == 'Status'):
					furnishing = data[i-1]
				elif(data[i] == 'Security Deposit'):
					deposit = int(data[i-1].replace(',',''))
		except:
			pass
        
		description = ''
		try:
			description = response.xpath('//div[@class="overview-wrap"]//span[@class="txt-desc js-desc js-desk"]//text()').extract()[0]
		except:
			pass

		property_info = ''
		additional_rooms = bathrooms = ''
		try:
			property_info = response.xpath('//div[@class="kd-wrap js-list-wrap"]//text()').extract()
			
			for i in range(0, len(property_info)):
				if(property_info[i] == 'Bathrooms'):
					bathrooms = int(property_info[i+1])
				elif(property_info[i] == 'Additional Rooms'):
					additional_rooms = property_info[i+1]
		except:
			pass

		address = ''
		total_area = ''
		price = -1
		try:
			address = ''.join(response.xpath('//div[@class="loc-wrap"]//text()').extract())
			total_area = response.xpath('//span[@class="size"]//text()').extract()[0]
			price = int(response.xpath('//span[@class="price"]//text()').extract()[0].replace(',',''))
			total_area = int((total_area.replace(',','').split(' '))[0])
			
		except:
			pass

		posted_by = ''
		try:
			posted_by = response.xpath('//span[@itemprop="legalName"]//text()').extract()
			print "\n\n\n\n\n", posted_by, '\n\n\n\n'
		except:
			pass

		project_name = ''
		try:
			project_name = response.xpath('//div[@class="project-wrap"]/text()').extract()
			print '\n\n\n\n\n', project_name, '\n\n\n'
		except:
			pass



		yield {'data' : data, 'furnishing' : furnishing, 'deposit' : deposit,
			'availaiblity': availaiblity, 'description' : description, 'bathrooms' : bathrooms, 
			'additional_rooms':additional_rooms, 'address': address, 'price':price,
			'total_area': total_area, 'posted_by' : posted_by
		}
