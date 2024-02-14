from django.forms import ModelForm

from library.models import UserReview

class ReviewForm(ModelForm):
    class Meta:
        model = UserReview
        fields = ['review']