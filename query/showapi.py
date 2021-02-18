import requests
import json
from book_store import BookStore
from query.queryer import Queryer
import time


class ShowApiQueryer(Queryer):
    def __init__(self, url, appid, secret, filename):
        super(ShowApiQueryer, self).__init__(filename)
        self.url = url
        self.appid = appid
        self.secret = secret
        self.headers = {"Content-Type": "application/x-www-form-urlencoded"}
        self.convert_rule = {
            "出版时间": "pubdate",
            "书名": "title",
            "定价": "price",
            "出版社": "publisher",
            "ISBN": "isbn",
            "作者": "author",
            "简介": "gist",
        }
        self.isbn = ""


    def query_from_api(self, isbn):
        time.sleep(0.2)
        r = requests.get(self.url, params={"showapi_appid": self.appid,
                                           "showapi_sign": self.secret,
                                           "isbn": isbn},
                         headers=self.headers
                         )
        if r.status_code != 200:
            self.failed_books.append(isbn)
            print("查询数据错误，isbn:{}, 错误码: {}".format(isbn, r.status_code))
            return {}

        res = json.loads(r.text).get("showapi_res_body")
        ret_code = res["ret_code"]
        if ret_code == 0:
            res_data = res["data"]
            return self.convert_to_book(res_data)
        elif ret_code == -1:
            self.missing_books.append(isbn)
            print("查询数据错误，isbn:{}, 错误内容: {}".format(isbn, res['remark']))
            return {}


if __name__ == '__main__':
    queryer = ShowApiQueryer("https://route.showapi.com/1626-1", "535975", "bd84cbad633b450bafbf9a775076f922")
    response = queryer.query_book("9787532756278")
    print(response)
