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
from core.mailer import sendMail

from library.models import BorrowRecord
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
        amount = form.cleaned_data['amount']
        account.balance += amount
        account.save()
        messages.success(self.request, 'Deposit success')
        user = self.request.user
        ctx = {
            'title':'Hello '+user.first_name+',',
            'body':'Your deposit of $'+str(amount)+' was successful.'
        }
        sendMail(self.request.user.email,'Deposit Success','email.html',ctx)
        return super().form_valid(form)


@login_required
def accountView(req):
    account = LibraryAccount.objects.filter(user=req.user).get()
    borrowRecords = BorrowRecord.objects.filter(
        user=req.user).order_by('borrowDate').reverse().all()
    ctx = {
        'account': account,
        'records': borrowRecords
    }
    return render(req, 'account.html', context=ctx)
