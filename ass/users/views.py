from django.forms import Form, ModelForm
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.contrib.auth import logout
from django.views.generic import FormView
from django.urls import reverse_lazy
from .forms import DepositForm, SignupForm
from users.models import LibraryAccount

# Create your views here.


class UserLoginView(LoginView):
    template_name = 'form.html'

    def get_success_url(self):
        return reverse_lazy('browseBooks')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Login'
        context["btnTxt"] = 'Login'
        return context


class RegistrationView(FormView):
    template_name = 'form.html'
    form_class = SignupForm
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Register'
        context["btnTxt"] = 'Submit'
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Registration successful')
        return super().form_valid(form)


@login_required
def logoutView(req: HttpRequest):
    logout(req)
    messages.success(req, 'Successfully logged out')
    return redirect('browseBooks')


class DepositView(LoginRequiredMixin, FormView):
    template_name = 'form.html'
    form_class = DepositForm
    success_url = reverse_lazy('account')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Deposit'
        context["btnTxt"] = 'Confirm'
        return context

    def form_valid(self, form: DepositForm):
        account = LibraryAccount.objects.filter(user=self.request.user).get()
        account.balance += form.cleaned_data['amount']
        account.save()
        messages.success(self.request, 'Deposit success')
        return super().form_valid(form)


@login_required
def accountView(req):
    account = LibraryAccount.objects.filter(user=req.user).get()
    ctx = {
        'account': account
    }
    return render(req, 'account.html', context=ctx)
