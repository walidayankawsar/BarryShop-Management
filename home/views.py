from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages
from django.conf import settings
from random import randint
from . models import VerifiCode, Employee
from django.core.mail import send_mail


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
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        user_has_error = False

        if User.objects.filter(username=phone).exists():
            user_has_error = True
            messages.error(request, "Phone Number are exists")
            
        if User.objects.filter(email=email).exists():
            user_has_error = True
            messages.error(request, "Email Address are exists")

        if len(password) < 5:
            user_has_error = True
            messages.error(request, "Password must be at least 5 characters")
        if password != confirm_password:
            user_has_error = True
            messages.error(request, "Password not match")

        if not user_has_error:
            new_user = User.objects.create_user(
                username= email,
                first_name = first_name,
                last_name = last_name,
                email = phone,
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
    if request.method=='POST':
        email = request.POST.get('email')
        request.session['email'] = email


        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, f'NO User found email {email}')
            return redirect('forget')
        code = f"{randint(0,999999):06d}"
        VerifiCode.objects.create(user=user, code = code)


        send_mail(
            "Your verification code",
            f"Code : { code } \n Verification code for your account. It's valid for one minute.",
            None,
            [email]
        )
        return redirect('verifacation')

    return render(request, 'authentication/BarryShop_forget1.html')

def verifacation(request):

    email = request.session.get('email')
    if not email:
        messages.error(request, "Session expired. Please try again.")
        return redirect('login')
    
    user = get_object_or_404(User, email=email)
    
    if request.method == 'POST':
        code_input = request.POST.get('code')

        try:
            vc = VerifiCode.objects.filter(user=user, used=False).latest('created_at')
        except VerifiCode.DoesNotExist:
            messages.error(request, 'Invalid or expired code.')
            return render(request, 'forget')
        
        if vc.code == code_input and not vc.is_expired():
            vc.used = True
            vc.save()

            messages.success(request, "Code Verified successful")
            return redirect('new_pass')
        else:
            messages.error(request, 'Incorrect or expired code')
            return redirect('forget')

    return render(request, 'authentication/BarryShop_forget2.html')


def new_pass(request):
    email = request.session.get('email')
    if not email:
        messages.error(request, "Session expired. Try again.")
        return redirect('login')
    
    user = User.objects.get(email=email)

    if request.method == 'POST':
        password = request.POST.get('newPassword')
        confirm_password = request.POST.get('confirmPassword')

        if password != confirm_password:
            messages.error(request, 'Passwords do not Match..!')
            return redirect('new_pass')
        user.set_password(password)
        user.save()
        messages.error(request, 'Password changed successfully..!')
        del request.session['email']
        return redirect('messages')


    return render(request, 'authentication/BarryShop_forget3.html')


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

