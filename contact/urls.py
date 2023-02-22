from django.urls import path
from .views import ContatView

urlpatterns = [
    path('', ContatView.as_view(), name='contact')
]
