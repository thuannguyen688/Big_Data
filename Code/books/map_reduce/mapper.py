import csv
import json
import sys
import io

csv_reader = csv.reader(sys.stdin, delimiter='$')
# sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
# csv_reader = csv.reader(sys.stdin)
list_books = []
for row in csv_reader:
    title = row[0]
    img_url = row[1]
    rating = row[2]
    price = row[3]
    status = row[4]
    desc = row[5]
    upc = row[6]
    product_type = row[7]
    price_excl = row[8]
    price_incl = row[9]
    tax = row[10]
    availability = row[11]
    number_of_reviews = row[12]
    type_of_book = row[13]
    book = {
        "title": title,
        "img_url": img_url,
        "rating": rating,
        "price": price,
        "status": status,
        "desc": desc,
        "upc": upc,
        "product_type": product_type,
        "price_excl": price_excl,
        "price_incl": price_incl,
        "tax": tax,
        "availability": availability,
        "number_of_reviews": number_of_reviews,
        "type_of_book": type_of_book
    }
    list_books.append(book)
    # print(f"title:{title}")
    # print(f"img_url:{img_url}")
    # print(f"rating:{rating}")
    # print(f"price:{price}")
    # print(f"status:{status}")
    # print(f"desc:{desc}")
    # print(f"upc:{upc}")
    # print(f"product_type:{product_type}")
    # print(f"price_excl:{price_excl}")
    # print(f"price_incl:{price_incl}")
    # print(f"tax:{tax}")
    # print(f"availability:{availability}")
    # print(f"number_of_review:{number_of_reviews}")
json_Book = json.dumps(list_books)
print(json_Book)