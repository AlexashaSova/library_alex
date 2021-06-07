# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User



class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    telephone_num = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Book(models.Model):
    id_category_id = models.ForeignKey('Category', models.DO_NOTHING)
    book_name = models.CharField(max_length=256)
    book_author = models.CharField(max_length=256)
    book_description = models.CharField(max_length=600)
    book_amount = models.IntegerField()
    book_price = models.DecimalField(max_digits=10, decimal_places=0)
    book_available = models.CharField(max_length=20)
    book_image = models.CharField(max_length=256)

    class Meta:
        db_table = 'book'

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.id = None

    def __str__(self):
        return '({}) {}'.format(self.id, self.book_name)

class Category(models.Model):
    category_name = models.CharField(unique=True, max_length=50)


    class Meta:
        db_table = 'category'

    def __str__(self):
        return '{}'.format(self.category_name)


class Delivery(models.Model):
    client_address = models.CharField(max_length=256)

    class Meta:
        db_table = 'delivery'

    def __str__(self):
        return '{}'.format(self.client_address)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Purchase(models.Model):
    id_status = models.ForeignKey('Status', models.DO_NOTHING, db_column='id_status', blank=True, null=True)
    id_user = models.ForeignKey(User, models.DO_NOTHING, db_column='id_user')
    id_delivery = models.ForeignKey(Delivery, models.DO_NOTHING, db_column='id_delivery', blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    payment_type = models.CharField(max_length=50, blank=True, null=True)
    expire_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'purchase'


class PurchaseHasBook(models.Model):
    id_book = models.ForeignKey(Book, models.DO_NOTHING, db_column='id_book')
    id_purchase = models.ForeignKey(Purchase, models.DO_NOTHING, db_column='id_purchase')
    amount = models.IntegerField()
    price = models.IntegerField()

    class Meta:
        db_table = 'purchase_has_book'


class Status(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'status'

    def __str__(self):
        return '{}'.format(self.name)