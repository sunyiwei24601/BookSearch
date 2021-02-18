import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class BookStore():
    def __init__(self, filename='book.db'):
        self.conn = sqlite3.connect(filename)
        self.conn.row_factory = dict_factory

    def init_db(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS book
           (    ISBN            VARCHAR(13)    PRIMARY KEY NOT NULL,
                书名            TEXT            NOT NULL,
               出版时间          VARCHAR(50),
               定价               VARCHAR(50),
               出版社              VARCHAR(100),
               作者               VARCHAR(100),
               简介             TEXT
               );
        ''')
        self.conn.commit()

        return self

    def get_book_info(self, isbn):
        return self.select(isbn)

    def update_book_info(self, book_info):
        isbn = book_info['ISBN']
        c = self.conn.cursor()
        cursor = c.execute('SELECT * from BOOK where ISBN = ?', (isbn,))
        if len(list(cursor)) < 1:
            self.insert(book_info)
        else:
            self.update(book_info)
        pass

    def insert(self, book_info):
        c = self.conn.cursor()
        book = (book_info.get("ISBN", ""), book_info.get("书名", ""),
                book_info.get("出版时间", ""), book_info.get("定价", ""),
                book_info.get("出版社", ""), book_info.get("作者", ""),
                book_info.get("简介", "")
                )
        c.execute('INSERT INTO BOOK  VALUES (?,?,?,?,?,?,?)', book)
        self.conn.commit()

    def update(self, book_info):
        c = self.conn.cursor()
        book = (book_info.get("书名", ""),
                book_info.get("出版时间", ""), book_info.get("定价", ""),
                book_info.get("出版社", ""), book_info.get("作者", ""),
                book_info.get("简介", ""),book_info.get("ISBN", "")
                )

        c.execute('''
            Update Book set 书名 = ?, 出版时间 = ?, 定价 = ?, 出版社 = ?,
            作者 = ?, 简介 = ? Where ISBN = ?
        ''', book)
        self.conn.commit()

    def select(self, isbn):
        c = self.conn.cursor()
        cursor = c.execute('SELECT * from BOOK where ISBN = ?', (isbn,))
        row = cursor.fetchone()
        return row


if __name__ == '__main__':
    store = BookStore().init_db()
    book = {
        "edition": "1",
        "paper": "胶版纸",
        "pubdate": "2017-07",
        "img": "http://static1.showapi.com/app2/isbn/508/ace8343336e14c3db9fb1c6f0d64724e.jpg",
        "gist": "《城市意象》是城市设计的开山之作。 作者凯文 林奇首次提出了 城市意象 的概念。 一座城市，无论景象多么普通，都可以给人带来欢乐。从《城市意象》这本书中我们发现，城市如同建筑，是一种空间的结构，只是尺度更巨大，需要用更长的时间过程去感知。城市设计可以说是一种时间的艺术，然而它与别的时间艺术，比如已掌握的音乐规律完全不同。很显然，不同的条件下，对于不同的人群，城市设计的规律有可能被倒置、打断、甚至是彻底废弃。",
        "format": "16开",
        "publisher": "华夏出版社",
        "author": "（美）凯文?林奇 Kevin Lynch",
        "title": "城市意象",
        "price": "35.00",
        "page": "",
        "isbn": "9787508091884",
        "binding": "平装-胶订",
        "produce": ""
    }
    store.update_book_info(book)
    print(store.select("9787508091884"))
