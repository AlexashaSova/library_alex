from django.conf.urls import url
from django.contrib import admin
from . import views
from . import forms
admin.autodiscover()

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'login/$', forms.AuthForm.as_view(), name= 'login'),
    url(r'register/$', forms.RegisterFormView.as_view(), name='register'),
    url(r'logout/$', views.logout_user, name = 'logout'),
    url(r'adminpanel/$', views.manage_products, name='adminpanel'),
    url(r'add_book/$', views.addBook, name='addBook'),
    url(r'nonfiction/$', views.nonfiction, name='nonfiction'),
    url(r'biography/$', views.biography, name='biography'),
    url(r'foreignliterature/$', views.foreignliterature, name='foreignliterature'),
    url(r'poetry/$', views.poetry, name='poetry'),
    url(r'novels/$', views.novels, name='novels'),
    url(r'fantasy/$', views.fantasy, name='fantasy'),
    url(r'philosophy/$', views.philosophy, name='philosophy'),
    url(r'^book_page/(?P<id_book>\w+)/$', views.book_page, name='book_page'),
    url(r'^change_book/(?P<id_book>\w+)/$', views.change_book, name='change_book'),
    url(r'^delete_book/(?P<id_book>\w+)/$', views.delete_book, name='delete_book'),
    url(r'cart/$', views.get_cart, name='cart'),
    url(r'^delete_from_cart/(?P<id_book>\w+)/$', views.delete_from_cart, name='delete_from_cart'),
    url(r'^delete_from_cart_view/(?P<id_book>\w+)/$', views.delete_from_cart_view, name='delete_from_cart_view'),
    url(r'makeorder/$', views.makeorder, name='makeorder'),
    url(r'delivery/$', views.delivery, name='filldelivery'),
    url(r'myaccount/$', views.edit_personal_data, name='account'),
    url(r'cart_delete/$', views.cart_delete, name='cart_delete'),
    url(r'myorders/$', views.my_orders, name='my_orders'),
    url(r'admin_orders/$', views.admin_orders, name='admin_orders'),
    url(r'^order_info/(?P<id_purchase>\w+)/$', views.order_info, name='order_info'),
    url(r'adminpanel/query/$', views.query, name='query'),

]