from django.contrib.auth.models import User
from django.db import models


# Create your models here.
def get_email(self):
    return self.email


User.add_to_class("__str__",get_email)


class Book(models.Model):
    name = models.CharField(max_length=100, null=False)
    author = models.CharField(max_length=100)
    book_count = models.IntegerField(default=0, null=False)

    def __str__(self):
        return self.name


class BorrowedBook(models.Model):
    book = models.ForeignKey(Book,
                             related_name="get_borrowed_book",
                             on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             related_name="get_user",
                             on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return self.user