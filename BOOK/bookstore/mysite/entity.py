class Book:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.id_category_id = kwargs.get('id_category_id')
        self.book_name = kwargs.get('book_name')
        self.book_author = kwargs.get('book_author')
        self.book_description = kwargs.get('book_description')
        self.book_amount = kwargs.get('book_amount')
        self.book_price = kwargs.get('book_price')
        self.book_available = kwargs.get('book_available')
        self.book_image = kwargs.get('book_image')

    def getData(self):
        return [self.id, self.id_category_id, self.book_name, self.book_author, self.book_description,
                self.book_amount, self.book_price, self.book_available, self.book_image]


class Delivery:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.client_address = kwargs.get('client_address')


class Purchase:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.id_user = kwargs.get('id_user')
        self.id_status = kwargs.get('id_status')
        self.id_delivery = kwargs.get('id_delivery')
        self.date = kwargs.get('date')
        self.payment_type = kwargs.get('payment_type')
        self.cart = kwargs.get('cart')
        self.delivery = kwargs.get('delivery')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.email = kwargs.get('email')
        self.expire_date = kwargs.get('expire_date')


    def getData(self):
        for items in vars(self).items():
            print(items)
        print(vars(self.delivery))
        print('Total', self.cart.total_price)
        print(self.cart.books)


class BookCart(Book):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cart_amount = kwargs.get('cart_amount')
        self.total_price = kwargs.get('total_price')

class User:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.username = kwargs.get('username')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.email = kwargs.get('email')
        self.telephone_num = kwargs.get('telephone_num')
    def getData(self):
        return [self.id, self.username, self.first_name, self.last_name, self.email, self.telephone_num]


class Cart:
    def __init__(self, books, id_cart):
        self.books = {}
        self.amount = 0
        self.total_price = 0
        self.id_cart = id_cart
        for book in books:
            self.amount += 1
            self.books[book.id] = book
            self.total_price += book.book_price * self.amount

    def getBooks(self):
        return self.books.values()


