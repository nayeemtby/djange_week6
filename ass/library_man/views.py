from django.shortcuts import redirect


def homeView(req):
    return redirect('browseBooks')