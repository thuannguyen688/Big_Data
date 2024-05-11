# MAPREDUCE

- ### File hướng dẫn: [Map_reduce.pdf](./Map_Reduce.pdf)

# TRUY VẤN PIG LATIN

- ### File code crawl data và mapreduce: [Code](Code/)
- ### Tải và xem nội cấu trúc bằng file excel: [books.xlsx](Data/books.xlsx)
- ### Tải và xem nội cấu trúc bằng file csv: [books.csv](Data/books.csv)
- ### Tải và xem nội cấu trúc bằng file json: [books.json](Data/books.json)

## Yêu cầu:

### 1. Sau khi crawl dữ liệu nên xuất ra file excel có cấu trúc các trường cách nhau bởi dấu `$` như sau:

```bash
title$img_url$rating$price$status$desc$upc$product_type$price_excl$price_incl$tax$availability$number_of_reviews$type_of_book
```

### 2. Để chạy được các lệnh hdfs và pig thì cần chạy lệnh sau:

```bash
start-all.sh
```

## Chuẩn bị:

### 1. Lưu dữ liệu từ local lên hdfs

```
hdfs dfs -put books.csv /books
```

### 2. Kiểm tra dữ liệu đã được lưu lên hdfs chưa

```
hdfs dfs -ls /books
```

## Hướng dẫn:

### Để chạy được lệnh pig thì cần chạy lệnh sau:

```bash
pig -x mapreduce
```

### 1. Đọc dữ liệu từ tệp books.csv với dấu phân cách là `$` và chuyển về các trường chính xác

```
books = LOAD '/books/books.csv' USING PigStorage('$') AS (title:chararray, img_url:chararray, rating:chararray, price:double, status:chararray, desc:chararray, upc:chararray, product_type:chararray, price_excl:double, price_incl:double, tax:double, availability:int, number_of_reviews:int, type_of_book:chararray);
```

### 2. Đếm số lượng sách

```
grouped_books = GROUP books ALL;
```
```
book_count = FOREACH grouped_books GENERATE COUNT(books) AS total_books;
```

```
DUMP book_count;
```

### 3. Lọc các sách có giá trên 50

```
expensive_books = FILTER books BY (price > 50.0);
```

```
DUMP expensive_books;
```

### 4. Lọc các sách có giá dưới 50

```
cheap_books = FILTER books BY (price < 50.0);
```

```
DUMP cheap_books;
```

### 5. Lọc các sách tồn kho > 10

```
available_books = FILTER books BY (availability > 10);
```

```
DUMP available_books;
```

### 6. Lọc các sách có số lượng đánh giá > 100

```
popular_books = FILTER books BY (number_of_reviews > 100);
```

```
DUMP popular_books;
```

### 7. Lọc các sách có số lượng đánh giá > 100 và giá trên 50

```
popular_expensive_books = FILTER books BY (number_of_reviews > 100 AND price > 50.0);
```

```
DUMP popular_expensive_books;
```

### 8. 5 sách có giá cao nhất

```
top_5_expensive_books = ORDER books BY price DESC;
top_5_expensive_books = LIMIT top_5_expensive_books 5;
```

```
DUMP top_5_expensive_books;
```

### 9. 5 sách có giá thấp nhất

```
top_5_cheap_books = ORDER books BY price ASC;
top_5_cheap_books = LIMIT top_5_cheap_books 5;
```

```
DUMP top_5_cheap_books;
```

### 10. Sắp xếp sách theo số lượng đánh giá giảm dần

```
books_by_reviews = ORDER books BY number_of_reviews DESC;
```

```
DUMP books_by_reviews;
```

### 11. Sắp xếp sách theo số lượng đánh giá tăng dần

```
books_by_reviews = ORDER books BY number_of_reviews ASC;
```

```
DUMP books_by_reviews;
```

### 12. Sắp xếp sách theo giá tăng dần

```
books_by_price = ORDER books BY price ASC;
```

```
DUMP books_by_price;
```

### 13. Sắp xếp sách theo giá giảm dần

```
books_by_price = ORDER books BY price DESC;
```

```
DUMP books_by_price;
```

### 14. Sắp xếp sách theo giá tăng dần và số lượng đánh giá giảm dần

```
books_by_price_reviews = ORDER books BY price ASC, number_of_reviews DESC;
```

```
DUMP books_by_price_reviews;
```

### 15. Sắp xếp sách theo giá giảm dần và số lượng đánh giá tăng dần

```
books_by_price_reviews = ORDER books BY price DESC, number_of_reviews ASC;
```

```
DUMP books_by_price_reviews;
```

### 16. Tổng tiền của tất cả sách

```
total_price = FOREACH (GROUP books ALL) GENERATE SUM(books.price) AS total_price;
```

```
DUMP total_price;
```

### 17. Tổng thể loại sách

```
type_of_books = GROUP books BY type_of_book;
```

```
DUMP type_of_books;
```

### 18. Tìm ra thể loại sách có số lượng sách nhiều nhất in ra tên thể loại và số lượng sách

```
max_books = ORDER count_books_type BY total_books DESC;
max_books = LIMIT max_books 1;
```

```
DUMP max_books;
```

### 19. Tìm ra thể loại sách có số lượng sách ít nhất in ra tên thể loại và số lượng sách

```
min_books = ORDER count_books_type BY total_books ASC;
min_books = LIMIT min_books 1;
```

```
DUMP min_books;
```

### 20. Tính tổng sách của từng thể loại sách in ra thể loại và tổng sách

```
grouped_books_type = GROUP books BY type_of_book;
count_books_type = FOREACH grouped_books_type GENERATE group AS type_of_book, COUNT(books) AS total_books;
```

```
DUMP count_books_type;
```
### 21. Lọc ra sách có giá bằng X hoặc Y
```
filter_books_XY = FILTER books BY (price == 51.77) or (price == 50.1);
```

```
DUMP filter_books_XY;
```
### 22. Tìm sách có title là: "A Light in the Attic"
```
book = FILTER books BY title == 'A Light in the Attic';
```

```
DUMP book;
```
### 23. Lưu data
```
STORE books INTO ' /myresult/books.txt ' USING PigStorage (',');
```

### 24. Kiểm tra data đã được lưu hay chưa
```
hdfs dfs -ls /myresult/books.txt
```
### 25. Đọc data đã lưu
```
hdfs dfs -cat /myresult/books.txt/part-*
```
### lưu ý: Từ 23 -> 25 làm theo đường dẫn thực tế của bài


## Tham khảo thêm tại trang web:

- [Apache Pig Tutorial](https://www.tutorialspoint.com/apache_pig/)
