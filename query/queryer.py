from book_store import BookStore


class Queryer:
    def __init__(self, filename='book.db'):
        self.missing_books = []
        self.failed_books = []
        self.output_book = []
        self.convert_rule = {}
        self.store = BookStore(filename=filename).init_db()

    # 按照一定规则，将response数据映射到表中的属性
    def convert_to_book(self, res_data):
        book = {}
        for key, value in self.convert_rule.items():
            book[key] = res_data.get(value, "")
        return book

    def query_from_db(self, isbn):
        return self.store.get_book_info(isbn)

    def query_book(self, isbn):
        book = self.query_from_db(isbn)
        if book is None or len(book.get("定价", "")) == 0:
            book = self.query_from_api(isbn)
            if len(book) != 0:
                self.store.update_book_info(book)
        if len(book.get("定价", "")) == 0:
            self.output_book.append(isbn)
        return book

    # 在子类中实现
    def query_from_api(self, isbn):
        return {}
        pass
