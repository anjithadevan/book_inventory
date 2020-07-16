from django.contrib import admin

# Register your models here.
from books.models import BorrowedBook, Book

admin.site.register(Book)
admin.site.register(BorrowedBook)