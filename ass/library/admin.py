from django.contrib import admin

from library.models import Book, BookCategory, BorrowRecord, UserReview

# Register your models here.

admin.site.register([BookCategory, Book, UserReview, BorrowRecord])
