from django.db import models

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    msg = models.TextField(blank=True, null=True)
