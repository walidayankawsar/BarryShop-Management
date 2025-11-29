from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class VerifiCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def is_expired(self):
        from django.utils import timezone
        from datetime import timedelta
        return timezone.now() > self.created_at + timedelta(seconds=60)
    
    class product(models.Model):


        priority_list = [
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ]

        category_list = [
            ("electronics", "Electronics"),
            ("groceries","Groceries"),
            ("fitness","Fitness"),
            ("unknown","Unknown"),
        ]

        user = models.ForeignKey(User, on_delete=models.CASCADE)
        barcode = models.IntegerField()
        title = models.CharField(max_length=260)
        price = models.DecimalField(max_digits=10, decimal_places=2)
        sku = models.CharField(max_length=50, unique=True, help_text="Stock Keeping Unit (unique identifier)")
        product_image = models.ImageField(upload_to='product_logos/', blank=True, null=True)
        is_complited = models.BooleanField(default=False)
        priority = models.CharField(max_length=10, choices=priority_list, default='medium')
        category = models.CharField(max_length=20, choices=category_list, default='unknown')
        created_at = models.DateTimeField(auto_now_add=True)