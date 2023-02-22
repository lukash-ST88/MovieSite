from django import forms

from .models import Reviews, StarsOfRating, Rating
from snowpenguin.django.recaptcha3.fields import ReCaptchaField


class ReviewsForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Reviews
        fields = ('email', 'name', 'text', 'captcha')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control border'}),
            'name': forms.TextInput(attrs={'class': 'form-control border'}),
            'text': forms.Textarea(attrs={'class': 'form-control border', 'id': "contactcomment"}),
        }

class RatingForm(forms.ModelForm):
    star = forms.ModelChoiceField(queryset=StarsOfRating.objects.all(), widget=forms.RadioSelect(), empty_label=None)

    class Meta:
        model = Rating
        fields = ('star',)
