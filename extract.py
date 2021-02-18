import csv
from query.showapi import ShowApiQueryer
import time


class BookList:
    def __init__(self, header=[]):
        self.bookList = {}
        self.header = header

    def extract_csv(self, filename, lines=10000):
        csv_file = open(filename, "r")
        reader = csv.DictReader(csv_file)
        for index, item in enumerate(reader):
            if index > lines:
                break
            isbn = item.get("ISBN", "").strip("'").strip()
            # 有ISBN以ISBN为主键，没有ISBN则以书名为主键
            if len(isbn) < 5:
                self.bookList[item.get("书名")] = item
            else:
                self.bookList[isbn] = item

        self.header = reader.fieldnames
        self.clean_header()
        csv_file.close()

    # 去除header中的空标题与错误标题
    def clean_header(self):
        # 删除空的header字段
        while "" in self.header:
            self.header.remove("")
        self.header.remove("2")

    # 从excel文件中提取数据
    def extract_excel(self, filename):
        pass

    def save_csv(self, filename):
        csv_file = open(filename, "w")
        writer = csv.DictWriter(csv_file, self.header)
        writer.writeheader()
        for book in self.bookList.values():
            row = {}
            for key in self.header:
                row[key] = book[key]
            writer.writerow(row)
        csv_file.close()

    def save_excel(self, filename):
        pass

    # 根据查询到的信息，更新原有数据，注意price若已经存在则不变
    def update_book(self, query_info):
        if len(query_info) == 0:
            return
        isbn = query_info['ISBN']
        book = self.bookList[isbn]
        price = book['定价']
        title = book['书名']

        book.update(query_info)
        if len(price.strip("")) >= 2:
            book["定价"] = price
        if len(title.strip()) >= 1:
            book['书名'] = title

        if len(book["定价"]) == 0:
            print("找不到定价， isbn:{}, query_info:{}".format(isbn, query_info))

    def generate_isbn(self):
        for i, key in enumerate(self.bookList):
            if len(key) == 13:
                yield key


if __name__ == '__main__':
    book_list = BookList()
    book_list.extract_csv("booklist.csv")
    queryer = ShowApiQueryer("https://route.showapi.com/1626-1", "535975", "bd84cbad633b450bafbf9a775076f922")
    for isbn in book_list.generate_isbn():
        time.sleep(0.3)
        queryer.query_book(isbn)

    book_list.save_csv("bookInfoList.csv")
