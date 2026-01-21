from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginView, name='login'),
    path('register/', views.RegisterView, name='register'),
    path('forget/', views.Forget, name='forget'),
    path('messages/', views.message, name='messages'),
    path('terms/', views.terms, name='terms'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('priceing/', views.priceing, name='priceing'),
    path('verifacation/', views.verifacation, name='verifacation'),
    path('new_password/', views.new_pass, name='new_pass'),

    path('home/', views.home, name='home'),
    path('settings/', views.settings, name='settings'),
    path('search/', views.search, name='search'),
    path('order/', views.order, name='order'),
    path('inventory/', views.inventory, name='inventory'),
    path('customers', views.customers, name='customer'),
    path('categories/', views.categories, name='categories'),
    path('barcode/', views.barcode, name='barcode'),
    path('logout/', views.user_logout, name='logout'),

    path('document/', views.doc_download, name='document'),
]