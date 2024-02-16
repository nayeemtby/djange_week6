from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.mailer import sendMail
from library.forms import ReviewForm

from library.models import Book, BookCategory, BorrowRecord, UserReview
from users.models import LibraryAccount

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


def bookDetailsView(req: HttpRequest, id):
    ctx: dict[str, object] = {}
    book = Book.objects.filter(pk=id).get()
    ctx['book'] = book
    if req.user.is_authenticated:
        hasBorrowedInThePast = BorrowRecord.objects.filter(
            user=req.user, book=book).count() > 0
        hasBorrowed = BorrowRecord.objects.filter(
            user=req.user, book=book, returned=False).count() > 0
        ctx['hasBorrowed'] = hasBorrowed
        ctx['hasBorrowedInThePast'] = hasBorrowedInThePast
    form = ReviewForm()
    if req.method == 'POST':
        form = ReviewForm(req.POST)
        form.instance.book = book
        form.instance.user = req.user
        if form.is_valid():
            form.save()
            form = ReviewForm()
    ctx['form'] = form
    ctx['comments'] = UserReview.objects.filter(book=book).all()
    return render(req, 'book_details.html', ctx)


@login_required
def borrowBookView(req: HttpRequest, id):
    book = Book.objects.filter(id=id).get()
    account = LibraryAccount.objects.filter(user=req.user).get()
    hasBorrowed = BorrowRecord.objects.filter(
        book=book, user=req.user, returned=False).count() > 0
    if account.balance < book.price:
        messages.error(
            req, "You don't have enough balance to borrow this book")
    elif hasBorrowed:
        messages.error(req,
                       'You have already borrowed this book which you have not returned yet.')
    else:
        account = LibraryAccount.objects.filter(user=req.user).get()
        BorrowRecord.objects.create(user=req.user, book=book, cost=book.price)
        account.balance -= book.price
        account.save()
        messages.success(req, 'You have successfully borrowed this book')
        user = req.user
        ctx = {
            'title':'Hello '+user.first_name+',',
            'body':'You have successfully borrowed the book "'+book.title+'".'
        }
        sendMail(user.email,'You just borrowed a book','email.html',ctx)

    return redirect('bookDetails', book.id)


@login_required
def returnBookView(req: HttpRequest, id):
    book = Book.objects.filter(id=id).get()
    account = LibraryAccount.objects.filter(user=req.user).get()
    record = BorrowRecord.objects.filter(
        book=book, user=req.user, returned=False).get()

    if record == None:
        messages.error(req,
                       'You have not borrowed this book yet')
    else:
        account.balance += record.cost
        record.returned = True
        record.save()
        account.save()
        messages.success(req, 'You have successfully returned this book')
    return redirect('bookDetails', book.id)
