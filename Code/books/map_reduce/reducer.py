# -*- coding: utf-8 -*-
import sys
import json
list_books = json.loads(sys.stdin.readline())

# 5 Sản phẩm giá cao nhất
list_books_sort = sorted(list_books, key=lambda x: float(x["price"]), reverse=True)
print([{"title": str(i["title"]), "price": float(i["price"]), "type_of_book": str(i["type_of_book"])} for i in list_books_sort[:5]])

# Sản phẩm còn tồn kho nhiều nhất
# list_books_sort = sorted(list_books, key=lambda x: int(x["availability"]), reverse=True)
# print([list_books_sort[:1]])

# Top 5 sản phẩm được đánh giá 5 sao