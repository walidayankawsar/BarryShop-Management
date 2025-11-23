from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages
from django.conf import settings


# Create your views here.

def loginView(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request=request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid Email Address or Password')
            return redirect("login")


    return render(request, 'authentication/BarryShop_login.html')

def RegisterView(request):

    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        phone = request.POST.get('phone')
        username = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        user_has_error = False

        if User.objects.filter(username=username).exists():
            user_has_error = True
            messages.error(request, "Email Address are exists")
        if User.objects.filter(email=phone).exists():
            user_has_error = True
            messages.error(request, "phone Number are exists")

        if len(password) < 5:
            user_has_error = True
            messages.error(request, "Password must be at least 5 characters")
        if password != confirm_password:
            user_has_error = True
            messages.error(request, "Password not match")

        if not user_has_error:
            new_user = User.objects.create_user(
                username= username,
                first_name = first_name,
                last_name = last_name,
                email = username,
                password = password
            )
            messages.success(request, 'Account created, LogIn Now...!')
            return redirect('messages')
        else:
            return redirect('register')

    return render(request, 'authentication/BarryShop_register.html')


def message(request):
    return render(request, 'authentication/BarryShop_messages.html')


def Forget(request):
    return render(request, 'authentication/BarryShop_forget1.html')


def terms(request):
    return render(request, 'Terms_and_conditions.html')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'About.html')

def profile(request):
    return render(request, 'pages/profile.html')

def priceing(request):
    return render(request, 'priceing.html')



def user_logout(request):
    logout(request)
    return redirect('login')








@login_required
def home(request):
    return render(request, 'index.html')

@login_required
def settings(request):
    return render(request, 'pages/settings.html')

@login_required
def product(request):
    return render(request, 'pages/product.html')

@login_required
def order(request):
    return render(request, 'pages/orders.html')

@login_required
def inventory(request):
    return render(request, 'pages/inventory.html')

@login_required
def customers(request):
    return render(request, 'pages/customers.html')

@login_required
def categories(request):
    return render(request, 'pages/categories.html')

@login_required
def barcode(request):
    return render(request, 'pages/barcode_manager.html')

