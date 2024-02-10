from django.shortcuts import render

# Create your views here.


def browseBooksView(req):
    return render(req, 'base.html')
