from django.core.files.storage import FileSystemStorage
from django.db import connection
from django.db.models import ImageField
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from .entity import *
from .entity import User as MyUser
#from .forms import AmountForm

from datetime import datetime
from django.utils.encoding import smart_str

class DAO:


    @staticmethod
    def getBookList(category=None):
        c = connection.cursor()
        result = []
        try:
            if category is None:
                c.execute("select id, id_category_id, book_name, book_author, book_description, book_amount, book_price, "
                          "book_available, book_image from book order by id desc")
            else:
                c.execute("select book.id, id_category_id,book.book_name, book_author, book_description, book_amount,"
                          " book_price, book_available,\
                 book_image from book join category on book.id_category_id = category.id where category.category_name = %s", [category])

            for id, id_category_id, name, author, description, amount,price, available, image in c.fetchall():
                result.append(Book(id=id, category = id_category_id, book_name = name, book_author = author, book_description = description, book_amount= amount, book_price = price, book_available=available, book_image = image))
        except Exception as ex:
            print(ex)
            return []
        finally:
            c.close()
        return result


    @staticmethod
    def get_user(id):
        c = connection.cursor()
        result = []
        try:
            c.execute("select id, username, first_name, last_name, email, telephone_num from auth_user where id = %s LIMIT 1",
                      [id])
            for id ,username, first_name, last_name, email, telephone_num in c.fetchall():
                result.append(
                    MyUser(id=id, username=username, first_name=first_name, last_name=last_name, email=email, telephone_num=telephone_num))
        except Exception as ex:
            print(ex)
        finally:
            c.close()
        if len(result) == 1:
            result = result[0]
        return result

    @staticmethod
    def update_user(user):
        c = connection.cursor()
        data = user.getData()
        try:
            c.execute("update auth_user set first_name = %s, last_name = %s, email = %s, telephone_num = %s where id = %s",
                      data[2:] + data[0:1])
        except Exception as ex:
            print(ex)
        finally:
            c.close()

    @staticmethod
    def get_products_for_admin():
        c = connection.cursor()
        result = []
        try:
            c.execute("select id,id_category_id, book_name, book_author, book_description, book_amount,"
                      " book_price, book_available, book_image from book order by id desc")
            for id, id_category_id, name, author, description, amount,price, available, image in c.fetchall():
                result.append(Book(id=id, category = id_category_id, book_name = name, book_author = author,
                                   book_description = description, book_amount= amount, book_price = price,
                                   book_available = available, book_image = image))
        except Exception as ex:
            print(ex)
            return []
        finally:
            c.close()
        return result



    @staticmethod
    def addNewBook(new_book):
        c=connection.cursor()
        new_book.id_category_id = smart_str(new_book.id_category_id)
        data = new_book.getData()[1:]
        try:
            c.execute("select id from category where category_name = %s", [data[0]])
            id = c.fetchone()[0]
            c.execute("insert into book (id_category_id, book_name, \
             book_author, book_description, book_amount, book_price, book_available,book_image)"
                      " values (%s, %s, %s, %s, %s, %s, %s, %s)", [id]+data[1:])
        except Exception as ex:
            print(ex)


    @staticmethod
    def get_book_by_id(book):
        c = connection.cursor()
        result = []
        try:
            c.execute("select id, id_category_id, book_name, book_author, book_description,"
                      " book_amount, book_price, book_available, book_image from book where id = %s LIMIT 1", [book])
            for id, id_category_id, name, author, description, amount,price, available, image in c.fetchall():
                result.append(Book(id=id, category = id_category_id, book_name = name, book_author = author,
                                   book_description = description, book_amount= amount, book_price = price,
                                   book_available=available, book_image = image))
        except Exception as ex:
            print(ex)
        finally:
            c.close()
        if len(result) == 1:
            result = result[0]
        else:
            result = Book()
        return result



    @staticmethod
    def update_product_by_id(id_book, book):
        c = connection.cursor()
        data = book.getData()[1:]
        print(131, id_book)
        try:
                c.execute('update book set id_category_id= %s, book_name= %s, \
             book_author= %s, book_description= %s, book_amount= %s, book_price= %s,'
                          ' book_available= %s,book_image= %s where id = %s', data + [id_book])
        except Exception as ex:
            print(ex)


    @staticmethod
    def delete_book_by_id(id_book):
        c = connection.cursor()
        try:
            c.execute('delete from book where id = %s', [id_book])
        except Exception as ex:
            print(ex)


    @staticmethod
    def search(book_name=None):
        c = connection.cursor()
        result = []
        if book_name is None:
            return result
        else:
            try:
                c.execute("select book.id, id_category_id,book.book_name, book_author, book_description, "
                          "book_amount, book_price, book_available,\
                     book_image from book where book_name = %s",
                          [book_name])
                for id, id_category_id, name, author, description, amount, price, available, image in c.fetchall():
                    result.append(Book(id=id, category=id_category_id, book_name=name, book_author=author,
                                   book_description=description, book_amount=amount, book_price=price,
                                   book_available=available, book_image=image))
            except Exception as ex:
                print(ex)
                return []
            finally:
                c.close()
            return result



    @staticmethod
    def make_query():
        c = connection.cursor()
        result = []
        try:
            c.execute('select sum(purchase_has_book.price) as temp, auth_user.username, auth_user.first_name, '
                      'auth_user.last_name from purchase_has_book \
join purchase on purchase_has_book.id_purchase = purchase.id \
join auth_user on purchase.id_user = auth_user.id \
where purchase.id_status = (select id from status where name ="Выполнен" LIMIT 1) and \
date between "20200607" and "20200608" group by username order by sum(purchase_has_book.price) asc;')
            result = c.fetchall()
        except Exception as ex:
            print(ex)
        finally:
            c.close()
        return result



    @staticmethod
    def create_purchase(id_user):
        c = connection.cursor()
        try:
            #if DAO.purchase_exists(id_user):
                #c.execute("delete from purchase where id_user = %s and id_status = %s", [id_user, 1])
            c.execute("insert into purchase (id_user, id_status) values (%s, %s)", [id_user, 1])
            c.execute("select id from purchase where id_user = %s and id_status = %s", [id_user, 1])
            id_purchase = c.fetchone()[0]
            cart = DAO.get_cart(DAO.create_cart(id_user))
            for book in cart.books.values():
                c.execute("insert into purchase_has_book(id_purchase, id_book, price, amount) values (%s, %s, %s, %s)",
                          [id_purchase, book.id, book.total_price, book.cart_amount])
            return id_purchase
        except Exception as ex:
            print(ex)
        finally:
            c.close()


    @staticmethod
    def purchase_exists(id):
        c = connection.cursor()
        try:
            c.execute("select count(*) from purchase where id_status = %s and id_user = %s LIMIT 1", [1, id])
            amount = c.fetchone()[0]
            return bool(amount)
        except Exception as ex:
            print(ex)
        finally:
            c.close()


    @staticmethod
    def cart_exists(id_user):
        c = connection.cursor()
        try:
            c.execute("select count(*) from purchase "
                      "where id_status is NULL and id_delivery is NULL and id_user = %s LIMIT 1", [id_user])
            amount = c.fetchone()[0]
            return bool(amount)
        except Exception as ex:
            print(ex)
        finally:
            c.close()


    @staticmethod
    def create_cart(id_user):
        c = connection.cursor()
        try:
            if not DAO.cart_exists(id_user):
                c.execute("insert into purchase (id_user) value (%s)", [id_user])
            c.execute("select id from purchase where id_status is NULL and id_user = %s LIMIT 1", [id_user])
            return c.fetchone()[0]
        except Exception as ex:
            print(ex)
        finally:
            c.close()

    @staticmethod
    def add_to_cart(id_user, book, amount):
        c = connection.cursor()
        try:
            id_cart = DAO.create_cart(id_user)
            c.execute("insert into purchase_has_book (id_purchase, id_book, price, amount) values (%s, %s, %s, %s)",
                      [id_cart, book.id, amount * book.book_price, amount])
        except Exception as ex:
            print(ex)
        finally:
            c.close()

    @staticmethod
    def delete_cart(id_user):
        c = connection.cursor()
        try:
            c.execute("delete from purchase where id_user = %s and id_status is NULL", [id_user])
        except Exception as ex:
            print(ex)

    @staticmethod
    def book_in_cart(id_user, book):
        c = connection.cursor()
        try:
            id_cart = DAO.create_cart(id_user)
            c.execute("select count(*) from purchase_has_book where id_purchase = %s and id_book = %s LIMIT 1", [id_cart, book.id])
            return bool(c.fetchone()[0])
        except Exception as ex:
            print(ex)
        finally:
            c.close()

    @staticmethod
    def update_book_amount(id_book, amount):
        c = connection.cursor()
        try:
            c.execute("update book set book_amount = %s where id = %s", [amount, id_book])
        except Exception as ex:
            print(ex)
        finally:
            c.close()

    @staticmethod
    def delete_from_cart(id_user, book):
        c = connection.cursor()
        try:
            id_cart = DAO.create_cart(id_user)
            if DAO.book_in_cart(id_user, book):
                c.execute("select amount from purchase_has_book where id_book = %s and id_purchase = %s",
                          [book.id, id_cart])
                amount = c.fetchone()[0]
                DAO.update_book_amount(book.id, book.book_amount + amount)
                c.execute("delete from purchase_has_book where id_book = %s and id_purchase = %s",
                          [book.id, id_cart])
        except Exception as ex:
            print(ex)
        finally:
            c.close()

    @staticmethod
    def get_cart(id_cart):
        c = connection.cursor()
        result = []
        cart = Cart(result, id_cart)
        try:
            c.execute("select book.id, book_name, book_author, book_description, book_amount, book_price, book_available, book_image, price, amount\
                                       from book join purchase_has_book on book.id = purchase_has_book.id_book \
                                        where id_purchase = %s", [id_cart])
            for id, book_name, book_author, book_description, book_amount, book_price, available, image, total_price, cart_amount in c.fetchall():
                result.append(
                    BookCart(id=id, book_name = book_name, book_author = book_author, book_description = book_description, book_amount= book_amount, book_price = book_price, book_available= available, book_image = image, total_price = total_price, cart_amount=cart_amount))
            cart = Cart(result, id_cart)
        except Exception as ex:
            print(ex)
        finally:
            c.close()
        return cart


    @staticmethod
    def update_price_in_cart(id_cart):
        c = connection.cursor()
        cart_total = connection.cursor()
        result = []
        try:
            c.execute("select id_book, amount from purchase_has_book where id_purchase = %s", [id_cart])
            for id, amount in c.fetchall():
                cart_total.execute("select book_price from book where id = %s LIMIT 1", [id])
                price = cart_total.fetchone()[0]
                c.execute("update purchase_has_book set price = %s where id_purchase = %s", [price, id])
        except Exception as ex:
            print(ex)
        finally:
            c.close()
        return result


    @staticmethod
    def return_items(cart):
        c = connection.cursor()
        try:
            for book in cart.books.values():
                c.execute("update book set book_amount = %s where id = %s",
                          [book.book_amount + book.cart_amount, book.id])
        except Exception as ex:
            print(ex)


    @staticmethod
    def confirm(user):
        c = connection.cursor()
        try:
            if DAO.purchase_exists(user.id):
                c.execute("update purchase set id_status = (select id from status where name = 'Новый') \
                   where id_status = 1 and id_user = %s", [user.id])
                return True
            else:
                return False
        except Exception as ex:
            print(ex)

    @staticmethod
    def delivery(user, client_address):
        client_address = smart_str(client_address)
        c = connection.cursor()
        try:
            if DAO.purchase_exists(user.id):
                c.execute("select count(*) from delivery where client_address = %s LIMIT 1", [ client_address])
                if c.fetchone()[0] == 0:
                    c.execute("insert into delivery (client_address) \
                        values (%s)", [client_address])
                c.execute("select id from delivery where  client_address = %s LIMIT 1", [client_address])
                id = c.fetchone()[0]
                c.execute("update purchase set id_delivery = %s \
                                    where id_status = 1 and id_user = %s",
                          [id, user.id])
        except Exception as ex:
            print(ex)

    @staticmethod
    def order_data(user):
        c = connection.cursor()
        print([datetime.now(), user.id])
        try:
            if DAO.purchase_exists(user.id):
                c.execute("update purchase set date = %s \
                    where id_status = 1 and id_user = %s",
                          [datetime.now(), user.id])
        except Exception as ex:
            print(ex)


    @staticmethod
    def get_after_order(id_purchase):
        c = connection.cursor()
        result = []
        cart = Cart(result, id_purchase)
        try:
            c.execute("select  book.id, book_name, book_author, book_description, book_amount, book_price, book_available, book_image, price, amount\
                                           from book join purchase_has_book on book.id = purchase_has_book.id_book \
                                            where id_purchase = %s", [id_purchase])
            for id, book_name, book_author, book_description, book_amount, book_price, available, image, total_price, cart_amount in c.fetchall():
                result.append(
                    BookCart(id=id, book_name=book_name, book_author=book_author,
                             book_description=book_description, book_amount=book_amount, book_price=book_price,
                             book_available=available, book_image=image, total_price=total_price, cart_amount=cart_amount))
            cart = Cart(result, id_purchase)
        except Exception as ex:
            print(ex)
        finally:
            c.close()
        return cart



    @staticmethod
    def get_user_orders(user):
            c = connection.cursor()
            result = []
            try:
                c.execute("select purchase.id, id_user, status.name, id_delivery, payment_type, client_address, date, expire_date \
                          from purchase join status on id_status = status.id \
                          LEFT OUTER JOIN delivery on delivery.id = purchase.id_delivery \
                          where id_user = %s and id_status is not NULL and id_status != 1 order by purchase.id desc", [user])
                for id, id_user, id_status, id_delivery, payment_type, client_address, date, expire_date in c.fetchall():
                    result.append(Purchase(id=id, id_user = id_user, id_status =id_status,  id_delivery=id_delivery, date=date,
                                           expire_date=expire_date,
                                           delivery=Delivery(id=id_delivery, client_address=client_address), cart = DAO.get_after_order(id)))
            except Exception as ex:
                print(ex)
            finally:
                c.close()
            return result

    @staticmethod
    def get_orders( status = None):
        c = connection.cursor()
        result = []
        try:
            if status is not None:
                c.execute("select purchase.id, id_user, status.name, id_delivery, payment_type, client_address, date, expire_date \
                      from purchase join status on id_status = status.id \
                      LEFT OUTER JOIN delivery on delivery.id = purchase.id_delivery \
                      where id_status is not NULL and id_status != 1 order by purchase.id desc",
                      [status])
            else:
                c.execute("select purchase.id, id_user, status.name, id_delivery, payment_type, client_address, date, expire_date \
                                              from purchase join status on id_status = status.id \
                                              LEFT OUTER JOIN delivery on delivery.id = purchase.id_delivery \
                                              where id_status is not NULL and id_status != 1 order by purchase.id desc")

            for id, id_user, id_status, id_delivery, payment_type, client_address, date, expire_date in c.fetchall():
                result.append(
                    Purchase(id=id, id_user=id_user, id_status=id_status, id_delivery=id_delivery, date=date, expire_date=expire_date,
                             delivery=
                    Delivery(id=id, client_address=client_address), cart=DAO.get_after_order(id)))
        except Exception as ex:
            print(ex)
        finally:
            c.close()
        return result



    @staticmethod
    def get_all_statuses():
        c = connection.cursor()
        result = {}
        try:
            c.execute("select id, name from status")
            for id, status in c.fetchall():
                result[id] = status
        except Exception as ex:
            print(ex)
        finally:
            c.close()
        return result

    @staticmethod
    def set_status(purchase, id_status):
        c = connection.cursor()
        try:
            c.execute("update purchase set id_status = %s where id = %s", [id_status, purchase])
        except Exception as ex:
            print(ex)

    @staticmethod
    def get_purchase(id_purchase):
        c = connection.cursor()
        result = Purchase(id_delivery=Delivery(), cart=Cart([], None))
        try:
            c.execute("select purchase.id, id_user, status.name, id_delivery, payment_type, first_name, last_name, email, telephone_num,"
                      " client_address, date, expire_date \
                             from purchase join status on id_status = status.id join auth_user on id_user = auth_user.id \
                             LEFT OUTER JOIN delivery on delivery.id = purchase.id_delivery \
                             where purchase.id = %s and id_status is not NULL and id_status != 1 LIMIT 1",
                      [id_purchase])
            for id, id_user, id_status, id_delivery, payment_type, first_name,last_name, email, telephone_num, \
                client_address, date,expire_date\
        in c.fetchall():
                 result = Purchase(id=id, id_user=id_user, id_status=id_status,
                                id_delivery=id_delivery, payment_type=payment_type, first_name=first_name, last_name=last_name, email=email, telephone_num=telephone_num,
                                   date=date, expire_date= expire_date,
                               delivery=
                               Delivery(id=id_delivery, client_address=client_address),
                               cart=DAO.get_after_order(id))
        except Exception as ex:
            print('get_one_order')
            print(ex)
        finally:
            c.close()
        return result