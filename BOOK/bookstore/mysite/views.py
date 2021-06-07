from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .DAO import *
from .forms import *
from .models import Book
from .entity import User
from django.db.models import Q

from django.views.generic import *
from .entity import Book

def query(request):
    query = DAO.make_query()
    return render(request, '/adminpanel/query.html', locals())



def index(request):
    form = PostForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        book_name = form.cleaned_data.get('book_name')
        if book_name == '':
            books = DAO.getBookList()
        else:
            books = DAO.search(book_name)
        size = len(books)
        return render(request, 'mysite/index.html', locals())
    else:
        books = DAO.getBookList(category=None)
        size = len(books)
        return render(request, 'mysite/index.html', locals())


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    if user.is_superuser:
                        return redirect('/adminpanel')
                    else:
                        return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'mysite/login.html', {'form': form})



@login_required
def afterlogin(request):
    if request.user.is_active and request.user.is_superuser:
        return redirect('/adminpanel')
    else:
        return redirect('/')

@login_required
def logout_user(request):
    if request.user.is_active:
        logout(request)
    return redirect('/')


@login_required
def manage_products(request):
    if request.user.is_active and request.user.is_superuser:
        books = DAO.get_products_for_admin()
        return render(request, 'mysite/adminpanel.html', locals())
    else:
        return HttpResponse('Страница, которую Вы пытаетесь открыть, недоступна')


@login_required
def addBook(request):
    if request.user.is_active and request.user.is_superuser:
        if request.method == "POST":
            form = AddBookForm(request.POST, request.FILES)
            if form.is_valid():
                book = Book(
                    id=form.cleaned_data.get('id'),
                    id_category_id=form.cleaned_data.get('id_category_id'),
                    book_name=form.cleaned_data.get('book_name'),
                    book_author=form.cleaned_data.get('book_author'),
                    book_description=form.cleaned_data.get('book_description'),
                    book_amount=form.cleaned_data.get('book_amount'),
                    book_price=form.cleaned_data.get('book_price'),
                    book_available=form.cleaned_data.get('book_available'),
                    book_image=form.cleaned_data.get('book_image')
                )
                DAO.addNewBook(book)
                return redirect('/adminpanel')
            else:
                return render(request, 'mysite/add_book.html', locals())
        else:
            form = AddBookForm(None)
            return render(request, 'mysite/add_book.html', locals())
    else:
        return HttpResponse('Страница, которую Вы пытаетесь открыть, недоступна')


def nonfiction(request):
    books = DAO.getBookList('Документальная и учебная')
    size = len(books)
    return render(request, 'mysite/index2.html', locals())


def biography(request):
    books = DAO.getBookList('Биографии')
    size = len(books)
    return render(request, 'mysite/index2.html', locals())


def foreignliterature(request):
    books = DAO.getBookList('Зарубежная проза')
    size = len(books)
    return render(request, 'mysite/index2.html', locals())


def poetry(request):
    books = DAO.getBookList('Поэзия')
    size = len(books)
    return render(request, 'mysite/index2.html', locals())


def novels(request):
    books = DAO.getBookList('Романы')
    size = len(books)
    return render(request, 'mysite/index2.html', locals())


def fantasy(request):
    books = DAO.getBookList('Фантастика')
    size = len(books)
    return render(request, 'mysite/index2.html', locals())


def philosophy(request):
    books = DAO.getBookList('Философия')
    size = len(books)
    return render(request, 'mysite/index2.html', locals())


def book_page(request, id_book):
    book = DAO.get_book_by_id(id_book)
    if book.id is not None:
        if request.method == "POST":
            form = AmountForm(1, book.book_amount, request.POST)
            if form.is_valid():
                num = form.cleaned_data.get('amount')
                book = DAO.get_book_by_id(id_book)
                if num <= book.book_amount:
                    DAO.add_to_cart(request.user.id, book, form.cleaned_data.get('amount'))
                    amount = book.book_amount-num
                    DAO.update_book_amount(id_book, amount)
                return redirect('/book_page/{}/'.format(id_book))
            else:
                in_cart = DAO.book_in_cart(request.user.id, book)
                if book.book_amount == 0:
                    return redirect('/book_page/{}/'.format(id_book))
                else:
                    return render(request, 'mysite/book_page.html', locals())
        else:
            initial = {'amount': 1}
            form = AmountForm(1, book.book_amount, initial = initial)
            in_cart = DAO.book_in_cart(request.user.id, book)
            return render(request, 'mysite/book_page.html', locals())
    else:
        return HttpResponse('Страница, которую Вы пытаетесь открыть, недоступна')


@login_required
def change_book(request, id_book):
    if request.user.is_active and request.user.is_superuser:
        book = DAO.get_book_by_id(id_book)
        initial_dict = {
            'id_category_id': book.id_category_id,
            'book_name': book.book_name,
            'book_author': book.book_author,
            'book_description': book.book_description,
            'book_amount': book.book_amount,
            'book_price': book.book_price,
            'book_available': book.book_available,
            'book_image': book.book_image,
        }
        if request.method == "POST":
            form = ChangeBookForm(request.POST, request.FILES)
            if form.is_valid():
                book = Book(id=form.cleaned_data.get('id'),
                            id_category_id=form.cleaned_data.get('id_category_id'),
                            book_name=form.cleaned_data.get('book_name'),
                            book_author=form.cleaned_data.get('book_author'),
                            book_description=form.cleaned_data.get('book_description'),
                            book_amount=form.cleaned_data.get('book_amount'),
                            book_price=form.cleaned_data.get('book_price'),
                            book_available=form.cleaned_data.get('book_available'),
                            book_image=form.cleaned_data.get('book_image'))
                DAO.update_product_by_id(id_book, book)
                return redirect('/adminpanel')
            else:
                return render(request, 'mysite/change_book.html', locals())
        else:
            form = ChangeBookForm(initial=initial_dict)
            return render(request, 'mysite/change_book.html', locals())
    else:
        return HttpResponse('Страница, которую Вы пытаетесь открыть, недоступна')


@login_required
def delete_book(request, id_book):
    if request.user.is_active and request.user.is_superuser:
        DAO.delete_book_by_id(id_book)
        return redirect('/adminpanel')
    else:
        return HttpResponse('Страница, которую Вы пытаетесь открыть, недоступна')

    # КОРЗИНА


@login_required
def get_cart(request):
    if request.user.is_active and not request.user.is_superuser:
        id_cart = DAO.create_cart(request.user.id)
        DAO.update_price_in_cart(id_cart)
        cart = DAO.get_cart(id_cart)
        books = cart.getBooks()
        return render(request, 'mysite/cart.html', locals())
    else:
        return HttpResponse('Страница, которую Вы пытаетесь открыть, недоступна')


@login_required
def delete_from_cart(request, id_book):
    if request.user.is_active and not request.user.is_superuser:
        book = DAO.get_book_by_id(id_book)
        DAO.delete_from_cart(request.user.id, book)
        return redirect('/cart'.format(id_book))
    else:
        return HttpResponse('Страница, которую Вы пытаетесь открыть, недоступна')

@login_required
def delete_from_cart_view(request, id_book):
    if request.user.is_active and not request.user.is_superuser:
        book = DAO.get_book_by_id(id_book)
        DAO.delete_from_cart(request.user.id, book)
        return redirect('/cart')
    else:
        return HttpResponse('Страница, которую Вы пытаетесь открыть, недоступна')









@login_required
def makeorder(request):
    if request.user.is_active and not request.user.is_superuser:
        user = DAO.get_user(request.user.id)
        if request.method == "POST":
            form = OrderForm(request.POST)
            if 'with' in request.POST:
                if form.is_valid():
                    user = User(id=request.user.id,
                                first_name=form.cleaned_data.get('first_name'),
                                last_name=form.cleaned_data.get('last_name'),
                                email=form.cleaned_data.get('email'),
                                telephone_num=form.cleaned_data.get('telephone_num'))
                    DAO.order_data(user)
                    return redirect('/delivery')
                else:
                    return render(request, 'mysite/new_order.html', locals())
            else:
                if form.is_valid():
                    user = User(id=request.user.id,
                                first_name=form.cleaned_data.get('first_name'),
                                last_name=form.cleaned_data.get('last_name'),
                                email=form.cleaned_data.get('email'),
                                telephone_num=form.cleaned_data.get('telephone_num'))
                    DAO.order_data(user)
                    if DAO.confirm(user):
                        DAO.delete_cart(request.user.id)
                    return redirect('/myorders')
                else:
                    return render(request, 'mysite/new_order.html', locals())
        else:
            DAO.create_purchase(request.user.id)
            form = OrderForm()
            return render(request, 'mysite/new_order.html', locals())
    else:
        return HttpResponse('Страница, которую Вы пытаетесь открыть, недоступна')



@login_required
def look_account(request):
    if request.user.is_active:
        user = DAO.get_user(request.user.id)
        initial_dict = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'telephone_num':user.telephone_num
        }
        if request.method == "POST":
            form = ProfileChangeForm(request.POST)
            if form.is_valid():
                user = User(id = request.user.id,
                            first_name=form.cleaned_data.get('first_name'),
                            last_name=form.cleaned_data.get('last_name'),
                            email=form.cleaned_data.get('email'),
                            telephone_num=form.cleaned_data.get('telephone_num'))

                DAO.update_user(user)
                return redirect('/myaccount')
            else:
                return render(request, 'mysite/myaccount.html', locals())
        else:
            form = ProfileChangeForm(initial=initial_dict)
            return render(request, 'mysite/myaccount.html', locals())
    else:
        return HttpResponse('Страница, которую Вы пытаетесь открыть, недоступна')


@login_required
def my_orders(request):
    purchases = DAO.get_user_orders(request.user.id)
    size = len(purchases)
    return render(request, 'mysite/myorders.html', locals())



@login_required
def delivery(request):
    if request.user.is_active and not request.user.is_superuser:
        user = DAO.get_user(request.user.id)
        if request.method == "POST":
            form = DeliveryForm(request.POST)
            if form.is_valid():
                client_address = form.cleaned_data.get('client_address')
                DAO.delivery(user, client_address)
                if DAO.confirm(user):
                    DAO.delete_cart(request.user.id)
                return redirect('/myorders')
            else:
                return render(request, 'mysite/delivery.html', locals())
        else:
            form = DeliveryForm()
            return render(request, 'mysite/delivery.html', locals())
    else:
        return HttpResponse('Страница, которую Вы пытаетесь открыть, недоступна')


@login_required
def cart_delete(request):
    id_cart = DAO.create_cart(request.user.id)
    cart = DAO.get_cart(id_cart)
    DAO.return_items(cart)
    DAO.delete_cart(request.user.id)
    return redirect('/cart')



@login_required
def edit_personal_data(request):
    if request.user.is_active:
        user = DAO.get_user(request.user.id)
        initial_dict = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'telephone_num':user.telephone_num
        }
        if request.method == "POST":
            form = ProfileChangeForm(request.POST)
            if form.is_valid():
                user = User(id=request.user.id,
                            first_name=form.cleaned_data.get('first_name'),
                            last_name=form.cleaned_data.get('last_name'),
                            email=form.cleaned_data.get('email'),
                            telephone_num=form.cleaned_data.get('telephone_num'))
                DAO.update_user(user)
                return redirect('/myaccount')
            else:
                return render(request, 'mysite/myaccount.html', locals())
        else:
            form = ProfileChangeForm(initial=initial_dict)
            return render(request, 'mysite/myaccount.html', locals())
    else:
        return HttpResponse('Страница, которую Вы пытаетесь открыть, недоступна')





@login_required
def admin_orders(request):
    if request.user.is_active and request.user.is_superuser:
        purchases = DAO.get_orders()
        size = len(purchases)
        return render(request, 'mysite/admin_orders.html', locals())
    else:
        return HttpResponse('Страница, которую Вы пытаетесь открыть, недоступна')


@login_required
def order_info(request, id_purchase):
    if request.user.is_active:
        purchase = DAO.get_purchase(id_purchase)
        if purchase.id is None:
            print(422, "None", purchase.id)
            return HttpResponse('Страница, которую Вы пытаетесь открыть, недоступна')
        else:
            print(424, "not", purchase.id)
            choises = DAO.get_all_statuses()
            mas = []
            if purchase.id_status == "Ожидает комплектации":
                if purchase.id_delivery is None:
                    mas.append([3, choises.get(3)])
                    mas.append([6, choises.get(6)])
                else:
                    mas.append([3, choises.get(3)])
                    mas.append([5, choises.get(5)])
            elif purchase.id_status == "В пути":
                mas.append([4, choises.get(4)])
            elif purchase.id_status == "Выполнен":
                mas.append([5, choises.get(5)])
                mas.append([10, choises.get(10)])
            elif purchase.id_status == "Новый":
                mas.append([2, choises.get(2)])
                mas.append([3, choises.get(3)])
                mas.append([4, choises.get(4)])
            if request.method == "POST":
                form = StatusForm(mas, request.POST)
                if form.is_valid:
                    status = form.data.get('status')
                    books = purchase.cart.getBooks()
                    print(449, "order_nifo do", status.id)
                    if status in ('4', '10'):
                        print(450, "order_nifo", status.id)
                        DAO.return_items(purchase.cart)
                        DAO.set_status(purchase.id, status)
                    else:
                        DAO.set_status(purchase.id, status)
                    return redirect('/admin_orders')
                else:
                    return render(request, 'mysite/order_page.html', locals())
            else:
                form = StatusForm(mas)
                books = purchase.cart.getBooks()
                return render(request, 'mysite/order_page.html', locals())
    else:
        return HttpResponse('Страница, которую Вы пытаетесь открыть, недоступна')

