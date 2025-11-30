from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

class EmployeeManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# Create your models here.

class Employee(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20)
    email = models.EmailField(max_length=50, unique=True)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    profile = models.ImageField(upload_to='profile_pic/', blank=True, null=True)
    position = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = EmployeeManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'



class VerifiCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def is_expired(self):
        from django.utils import timezone
        from datetime import timedelta
        return timezone.now() > self.created_at + timedelta(seconds=60)
    

class Product(models.Model):

    priority_list = [
        ("in stock", "In Stock"),
        ("low stock", "Low Stock"),
        ("out of stock", "Out of Stock"),
    ]

    category_list = [
        ("electronics", "Electronics"),
        ("groceries","Groceries"),
        ("fitness","Fitness"),
        ("unknown","Unknown"),
        ("stationery","Stationery"),
        ("home & garden","Home & Garden"),
        ("clothing", "Clothing"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    barcode = models.CharField(max_length=20)
    title = models.CharField(max_length=260)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=50, unique=True, help_text="Stock Keeping Unit (unique identifier)")
    product_image = models.ImageField(upload_to='product_logos/', blank=True, null=True)
    is_complited = models.BooleanField(default=False)
    priority = models.CharField(max_length=20, choices=priority_list, default='low stock')
    category = models.CharField(max_length=20, choices=category_list, default='unknown')
    created_at = models.DateTimeField(auto_now_add=True)
