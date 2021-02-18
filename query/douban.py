from query.queryer import Queryer
import requests
import json
import time

class DouBanQueryer(Queryer):
    def __init__(self, filename='book.db'):
        super().__init__(filename)
        self.url = 'https://book.feelyou.top/isbn/'

    def query_from_api(self, isbn):
        time.sleep(1)
        url = self.url + isbn
        r = requests.get(url)
        if r.status_code != 200:
            self.failed_books.append(isbn)
            print("查询数据错误，isbn:{}, 错误码: {}".format(isbn, r.status_code))
            return {}

        res = json.loads(r.text)
        if res.get("error"):
            self.missing_books.append(isbn)
            print("查询错误， isbn:{}, 错误内容: {}".format(isbn, res.get("error")))
            return {}

        return self.convert_to_book(res)

    def convert_to_book(self, res_data):
        book = {
            "ISBN": res_data.get("isbn", ""),
            "书名": res_data.get("title", ""),
            "简介": res_data.get("book_intro", ""),
        }
        book_info = res_data.get("book_info")
        if book_info:
            book["作者"] = book_info.get("作者", "")
            book["出版社"] = book_info.get("出版社", "")
            book["出版时间"] = book_info.get("出版年", "")
            book["定价"] = book_info.get("定价", "")
        return book

if __name__ == '__main__':
    queryer = DouBanQueryer("../book.db")
    book = queryer.query_book("9787112167388")
    print(book)
