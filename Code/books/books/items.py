# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksItem(scrapy.Item):
    """
    Đại diện cho một mục sách được scrap từ một trang web.
    Thuộc tính:
        title: Tiêu đề của sách.
        img_url: URL của hình ảnh sách.
        rating: Đánh giá của sách.
        price: Giá của sách.
        status: Tình trạng của sách.
        desc: Mô tả về sách.
        upc: Mã sản phẩm phổ quát (UPC) của sách.
        product_type: Loại sản phẩm.
        price_excl: Giá của sách không bao gồm thuế.
        price_incl: Giá của sách bao gồm thuế.
        tax: Thuế được áp dụng cho sách.
        availability: Sự có sẵn của sách.
        number_of_reviews: Số lượng đánh giá cho sách.
        type_of_book: Thể loại.
    """
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
