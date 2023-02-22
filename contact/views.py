from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import ContactForm
from .models import Contact

class ContatView(CreateView):
    model = Contact
    form_class = ContactForm
    success_url = reverse_lazy('/')