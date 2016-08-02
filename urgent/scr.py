from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def magic():

	process = CrawlerProcess(get_project_settings())

	# 'followall' is the name of one of the spiders of the project.
	process.crawl('magic')
	process.start() # the script will block here until the crawling is fini

def acres():

	process = CrawlerProcess(get_project_settings())

	# 'followall' is the name of one of the spiders of the project.
	process.crawl('99acres')
	process.start() # the script will block here until the crawling is fini


def common():

	process = CrawlerProcess(get_project_settings())

	# 'followall' is the name of one of the spiders of the project.
	process.crawl('common')
	process.start() # the script will block here until the crawling is fini