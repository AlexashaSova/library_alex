from django.contrib import admin
from .models import *
# Register your models here.

class BookAdmin(admin.ModelAdmin):
    class Meta:
        model = Book

admin.site.register(Delivery)
admin.site.register(PurchaseHasBook)
admin.site.register(Status)
admin.site.register(Purchase)
admin.site.register(Book, BookAdmin)
admin.site.register(Category)