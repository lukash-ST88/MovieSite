from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    model = Contact
    fields = ('email', )
    widgets = {
        "email": forms.TextInput(attrs={'class': 'editContent'})
                }