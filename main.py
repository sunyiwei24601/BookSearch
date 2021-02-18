from query.showapi import ShowApiQueryer
from extract import BookList
from query.douban import DouBanQueryer
import time

if __name__ == '__main__':
    book_list = BookList()
    book_list.extract_csv("booklist.csv", 1300)
    showapi_queryer = ShowApiQueryer("https://route.showapi.com/1626-1", "535975", "bd84cbad633b450bafbf9a775076f922",
                                     "book.db")
    douban_queryer = DouBanQueryer()
    for index, isbn in enumerate(book_list.generate_isbn()):
        if index % 50 == 0:
            print("已经爬取第{}本书".format(index))
        if book_list.bookList[isbn].get("定价", "") != "":
            continue
        book = showapi_queryer.query_book(isbn)
        book_list.update_book(book)
        if len(book_list.bookList[isbn].get("定价", "")) == 0 and (
                book.get("定价") is None or len(book.get("定价")) == 0):
            book = douban_queryer.query_book(isbn)
            book_list.update_book(book)

    book_list.save_csv("bookInfoList.csv")
    pass
