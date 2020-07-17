from django.contrib import admin

# Register your models here.
from books.models import BorrowedBook, Book
from django.contrib.admin import AdminSite
from django.shortcuts import render
from django.http import HttpResponse


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'book_count')
    ordering = ('name',)
    search_fields = ('name',)


class MyAdminSite(AdminSite):
    model = Book

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        urls += [
            path('books/', self.admin_view(self.my_view))
        ]
        return urls

    def my_view(self, request):
        context = {}
        context["dataset"] = Book.objects.all()
        return render(request, "list_view.html", context)


admin_site = MyAdminSite()
# admin.site.register(Book)
admin.site.register(BorrowedBook)
