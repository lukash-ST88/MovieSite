from django.db import models

class Contact(models.Model):
    """подписка на email"""
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
