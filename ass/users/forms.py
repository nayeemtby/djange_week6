from django.contrib.auth.forms import UserCreationForm
from django.forms import Form, DecimalField
from django.contrib.auth.models import User
from .models import LibraryAccount


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',
                  'username', 'password1', 'password2']

    def save(self, commit: bool = True):
        if commit:
            user = super().save()
            LibraryAccount.objects.create(user=user)
            return user
        return super().save(commit)


class DepositForm(Form):
    amount = DecimalField(decimal_places=2, max_digits=12)