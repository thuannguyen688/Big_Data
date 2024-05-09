from typing import Iterable

import scrapy
from books.items import BooksItem
import re
from scrapy import Request


class BooksCrawlSpider(scrapy.Spider):
    name = "books_crawl"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def start_requests(self):
        yield scrapy.Request(url="https://books.toscrape.com/", callback=self.parse)

    def parse(self, response):
        book_crawl = response.xpath("//ol[@class='row']/li/article[@class='product_pod']")
        for index, book in enumerate(book_crawl):
            item = BooksItem()
            item["title"] = book.xpath('//h3/a/@title')[index].get()
            item["img_url"] = response.urljoin(book.xpath('//img[@class="thumbnail"]/@src')[index].get())
            item["rating"] = book.xpath('//p[contains(@class, "star-rating")]/@class')[index].get().split()[-1]
            item["price"] = float(book.xpath('//p[@class="price_color"]/text()')[index].get()[1:])
            item["status"] = book.xpath('//p[contains(@class,"instock")]/text()[normalize-space()]')[index].get().strip()
            # yield item

            # Lấy nội dung bên trong từng quyển sách
            detail_url = book.xpath('.//div[@class="image_container"]/a/@href').get()
            if detail_url:
                request = scrapy.Request(url=response.urljoin(detail_url), callback=self.detailBooks)
                request.meta["item"] = item
                yield request

        # Lấy tất cả các trang
        # next_page = response.xpath('//li[@class="next"]/a/@href').get()
        # if next_page:
        #     next_page_url = response.urljoin(next_page)
        #     yield scrapy.Request(url=next_page_url, callback=self.parse)

    # Hàm lấy nội dung bên trong
    def detailBooks(self, response):
        item = response.meta["item"]
        item["desc"] = response.xpath('//article[@class="product_page"]/p/text()').get()
        table = response.xpath('//tr/td/text()').getall()
        item["upc"] = table[0]
        item["product_type"] = table[1]
        item["price_excl"] = float(table[2][1:])
        item["price_incl"] = float(table[3][1:])
        item["tax"] = float(table[4][1:])
        # item["availability"] = table[5]
        # Lấy số lượng sách còn lại
        match = re.search(r'\d+', table[5])
        item["availability"] = int(match.group())
        item["number_of_reviews"] = int(table[6])
        item["type_of_book"] = response.xpath("//ul[@class='breadcrumb']/li[3]/a/text()").get()
        yield item

