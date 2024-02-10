from django.http import HttpRequest
from django.shortcuts import render

from library.models import Book, BookCategory

# Create your views here.


def browseBooksView(req: HttpRequest):
    cats = BookCategory.objects.all()
    requestedCat = req.GET.get('cat', None)
    books = []
    if requestedCat:
        books = Book.objects.filter(category=requestedCat).all()
    else:
        books = Book.objects.all()

    ctx = {
        'rc': requestedCat,
        'cats': cats,
        'books': books
    }

    return render(req, 'browse.html', context=ctx)
