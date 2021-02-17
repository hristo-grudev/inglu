import scrapy

from scrapy.loader import ItemLoader
from ..items import IngluItem
from itemloaders.processors import TakeFirst


class IngluSpider(scrapy.Spider):
	name = 'inglu'
	start_urls = ['https://www.ing.lu/webing/content/siteing/fr/About_us/press.html']

	def parse(self, response):
		post_links = response.xpath('//div[@class="panel panel-shadow-a h-bg-b-base "]')
		for post in post_links:

			link = post.xpath('.//h3[contains(@class, "-xl")]/a/@href').get()
			date = post.xpath('.//div[@class="text parbase section"]/p/text()|.//h3[contains(@class, "xxl")]/a/text()').get()
			if link and link[-3:] != 'pdf':
				yield response.follow(link, self.parse_post, cb_kwargs=dict(date=date))

	def parse_post(self, response, date):
		title = response.xpath('//h3[contains(@class, "heading-b-xxl h-text-b")]/text()').get()
		description = response.xpath('//div[@class="newsroomIntroduction title section"]//text()[normalize-space()]|//div[contains(@class, "text parbase")]//text()[normalize-space() and not(ancestor::div[@class="responsiverow section"])]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=IngluItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
