import csv
import json
import pymongo
import psycopg2
import mysql.connector

class ToCSV:
    def __init__(self):
        self.file = open('books.csv', 'w', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.file, delimiter="$")

        # Ghi tên các cột vào file CSV
        # columns = ['title', 'img_url', 'rating', 'price', 'status', 'desc', 'upc', 'product_type', 'price_excl', 'price_incl', 'tax', 'availability', 'number_of_reviews']
        # self.csv_writer.writerow(columns)

    def process_item(self, item, spider):
        # Ghi dữ liệu vào file CSV
        self.csv_writer.writerow([
            item.get('title'),
            item.get('img_url'),
            item.get('rating'),
            item.get('price'),
            item.get('status'),
            item.get('desc'),
            item.get('upc'),
            item.get('product_type'),
            item.get('price_excl'),
            item.get('price_incl'),
            item.get('tax'),
            item.get('availability'),
            item.get('number_of_reviews'),
            item.get("type_of_book")
        ])
        return item

    def close_spider(self, spider):
        self.file.close()


class ToJSON:
    def __init__(self):
        self.data = []

    def process_item(self, item, spider):
        self.data.append(dict(item))
        return item

    def open_spider(self, spider):
        self.file = open('books.json', 'w', encoding='utf-8')

    def close_spider(self, spider):
        json.dump(self.data, self.file, ensure_ascii=False, indent=4)
        self.file.close()

class MySQLPipeline:
    def __init__(self):
        self.connect = mysql.connector.connect(
            host='localhost',
            user='root',
            password='sapassword',
        )
        self.cursor = self.connect.cursor()
        # Kiểm tra xem cơ sở dữ liệu booksdb đã tồn tại
        self.cursor.execute("SHOW DATABASES LIKE 'booksdb'")
        db_exists = self.cursor.fetchone()
        # Nếu cơ sở dữ liệu tồn tại, xóa nó đi
        if db_exists:
            self.cursor.execute("DROP DATABASE booksdb")
        # Tạo cơ sở dữ liệu mới
        self.cursor.execute("CREATE DATABASE booksdb")
        # Sử dụng cơ sở dữ liệu booksdb
        self.cursor.execute("USE booksdb")
        # Tạo bảng books trong cơ sở dữ liệu
        self.cursor.execute("""
            CREATE TABLE books (
                id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
                title TEXT,
                image_url TEXT,
                rating TEXT,
                price FLOAT,
                status TEXT,
                description TEXT,
                upc TEXT,
                product_type TEXT,
                price_excl FLOAT,
                price_incl FLOAT,
                tax FLOAT,
                availability INTEGER,
                number_of_reviews INTEGER,
                type_of_book TEXT
            )
        """)

    def process_item(self, item, spider):
        self.cursor.execute('''
            INSERT INTO books (title, image_url, rating, price, status, description, upc, product_type, price_excl, price_incl, tax, availability, number_of_reviews, type_of_book)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (
            item['title'],
            item['img_url'],
            item['rating'],
            item['price'],
            item['status'],
            item['desc'],
            item['upc'],
            item['product_type'],
            item['price_excl'],
            item['price_incl'],
            item['tax'],
            item['availability'],
            item['number_of_reviews'],
            item.get("type_of_book")
        ))
        self.connect.commit()
        return item
    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()



class MongoDBPipeline:
    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.client['booksdb']
    def process_item(self, item, spider):
        collection = self.db['books']
        try:
            collection.insert_one(dict(item))
            return item
        except Exception as e:
            raise e



class PostgresPipeline:
    def __init__(self):
        self.connect = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='sapassword'
        )
        self.connect.set_session(autocommit=True)  # Thiết lập autocommit

        self.cursor = self.connect.cursor()

        # Kiểm tra xem cơ sở dữ liệu "booksdb" đã tồn tại
        self.cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'booksdb'")
        db_exists = self.cursor.fetchone()
        # Nếu cơ sở dữ liệu tồn tại, xóa nó đi
        if db_exists:
            self.cursor.execute("DROP DATABASE booksdb")
        # Tạo cơ sở dữ liệu mới
        self.cursor.execute("CREATE DATABASE booksdb")
        self.cursor.close()
        self.connect.close()
        #
        # # Kết nối đến cơ sở dữ liệu booksdb
        self.connect = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='sapassword',
            database='booksdb'
        )
        self.cursor = self.connect.cursor()

        # Tạo bảng books trong cơ sở dữ liệu booksdb
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                    id SERIAL PRIMARY KEY,
                    title TEXT,
                    image_url TEXT,
                    rating TEXT,
                    price FLOAT,
                    status TEXT,
                    description TEXT,
                    upc TEXT,
                    product_type TEXT,
                    price_excl FLOAT,
                    price_incl FLOAT,
                    tax FLOAT,
                    availability INTEGER,
                    number_of_reviews INTEGER,
                    type_of_book TEXT
            )
        """)

    def process_item(self, item, spider):
        self.cursor.execute('''
            INSERT INTO books (title, image_url, rating, price, status, description, upc, product_type, price_excl, price_incl, tax, availability, number_of_reviews, type_of_book)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (
            item['title'],
            item['img_url'],
            item['rating'],
            item['price'],
            item['status'],
            item['desc'],
            item['upc'],
            item['product_type'],
            item['price_excl'],
            item['price_incl'],
            item['tax'],
            item['availability'],
            item['number_of_reviews'],
            item.get("type_of_book")
        ))
        self.connect.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()