from django.db import models


class Contact(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True)
