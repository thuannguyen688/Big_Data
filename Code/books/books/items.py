# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksItem(scrapy.Item):
    title = scrapy.Field()
    img_url = scrapy.Field()
    rating = scrapy.Field()
    price = scrapy.Field()
    status = scrapy.Field()
    desc = scrapy.Field()
    upc = scrapy.Field()
    product_type = scrapy.Field()
    price_excl = scrapy.Field()
    price_incl = scrapy.Field()
    tax = scrapy.Field()
    availability = scrapy.Field()
    number_of_reviews = scrapy.Field()
    type_of_book = scrapy.Field()
