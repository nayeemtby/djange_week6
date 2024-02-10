from io import open_code
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


def _getFilePath(record, originalName):
    return f'uploads/{record.id}-{record.title}'


class BookCategory(models.Model):
    title = models.CharField(max_length=32)

    def __str__(self) -> str:
        return self.title


class Book(models.Model):
    category = models.ForeignKey(BookCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    image = models.ImageField(upload_to=_getFilePath)
    price = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    def __str__(self) -> str:
        return self.title+' - '+self.category.title


class UserReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    review = models.CharField(max_length=128)

class BorrowRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowDate = models.DateTimeField(auto_now_add=True)
    returned = models.BooleanField(default=False)
    cost = models.DecimalField(default=0, max_digits=12, decimal_places=2)
