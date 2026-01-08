from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages
from django.conf import settings
from random import randint
from . models import VerifiCode, Employee, Product, Category
from django.core.mail import send_mail
from .forms import CategoryForm
from django.db.models import Count


# Create your views here.

def loginView(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request=request, email=email, password=password)
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
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        user_has_error = False

        if Employee.objects.filter(username=username).exists():
            user_has_error = True
            messages.error(request, "Username are exists")
            
        if Employee.objects.filter(email=email).exists():
            user_has_error = True
            messages.error(request, "Email Address are exists")

        if Employee.objects.filter(phone=phone).exists():
            user_has_error = True
            messages.error(request, "Phone number are exists")

        if len(password) < 5:
            user_has_error = True
            messages.error(request, "Password must be at least 5 characters")
        if password != confirm_password:
            user_has_error = True
            messages.error(request, "Password not match")

        if not user_has_error:
            new_user = Employee.objects.create_user(
                username= username,
                first_name = first_name,
                last_name = last_name,
                email = email,
                password = password,
                phone = phone
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
            user = Employee.objects.get(email=email)
        except Employee.DoesNotExist:
            messages.error(request, f'NO User found {email}')
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
    
    user = get_object_or_404(Employee, email=email)
    
    if request.method == 'POST':
        code_input = request.POST.get('code')

        try:
            vc = VerifiCode.objects.filter(user=user, used=False).latest('created_at')
        except VerifiCode.DoesNotExist:
            messages.error(request, 'Invalid or expired code.')
            return redirect('forget')
        
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
    
    user = Employee.objects.get(email=email)

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

def priceing(request):
    return render(request, 'priceing.html')



def user_logout(request):
    logout(request)
    return redirect('login')








@login_required
def home(request):

    products = Product.objects.filter(user=request.user)
    product_list = products.count()
    in_stock = Product.objects.filter(user=request.user, priority='in stock').count()
    low_stock = Product.objects.filter(user=request.user, priority='low stock').count()
    out_of_stock = Product.objects.filter(user=request.user, priority='out of stock').count()

    categories = Category.objects.filter(user=request.user)

    if request.method == "POST":
        title = request.POST.get('title')
        sku = request.POST.get('sku')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        barcode = request.POST.get('barcode')

        image = request.FILES.get('image')

        from decimal import Decimal
        decimal_price = Decimal(price)
        qty = int(quantity)

        category_id = request.POST.get('category')
        category = None
        if category_id and category_id != "":
            try:
                category = Category.objects.get(id=category_id, user=request.user)
            except Category.DoesNotExist:
                pass


        if qty == 0:
            priority = 'out of stock'
        elif qty <= 5:
            priority = 'low stock'
        else:
            priority = 'in stock'

        try:
            if title:
                if Product.objects.filter(sku=sku).exists():
                    messages.error(request, "SKU already exists..try different SKU")
                else:
                    Product.objects.create(
                        user=request.user, 
                        barcode=barcode, 
                        title=title, 
                        price=decimal_price, 
                        quantity=qty, 
                        sku=sku, 
                        product_image=image, 
                        category=category,
                        priority=priority
                    )
                    messages.success(request, 'New product are added successfully')
                return redirect('home')
        except Exception:
            messages.error(request,"Unable to submit")
        return redirect('home')
    return render(request, 'index.html', {
        'product_list' : product_list,
        'out_of_stock' : out_of_stock,
        'in_stock' : in_stock,
        'low_stock' : low_stock,
        'products' : products,
        'categories' : categories
    })

@login_required
def settings(request):
    product_list = Product.objects.filter(user=request.user).count()
    return render(request, 'pages/settings.html', {'product_list': product_list})

'''@login_required
def search(request):
    product_list = Product.objects.filter(user=request.user).count()
    return render(request, 'pages/search.html', {'product_list':product_list})'''

@login_required
def order(request):
    product_list = Product.objects.filter(user=request.user).count()
    return render(request, 'pages/orders.html', {'product_list':product_list})

@login_required
def inventory(request):
    products = Product.objects.filter(user=request.user,)
    product_list =products.count()
    out_of_stock = Product.objects.filter(user=request.user, priority='out of stock').count()
    in_stock = Product.objects.filter(user=request.user, priority='in stock').count()
    low_stock =Product.objects.filter(user=request.user, priority='low stock').count()

    dynamic = {
        'product_list' : product_list,
        'out_of_stock' : out_of_stock,
        'in_stock' : in_stock,
        'low_stock' : low_stock,
        'products' : products
    }
    return render(request, 'pages/inventory.html', dynamic)

@login_required
def customers(request):
    product_list = Product.objects.filter(user=request.user).count()
    return render(request, 'pages/customers.html', {'product_list' : product_list})

@login_required
def categories(request):
    product_list = Product.objects.filter(user=request.user).count()
    categories_list = Category.objects.filter(user=request.user).annotate(
        product_count=Count('product')
    )



    # for editing a spacific category
    edit_category = None
    edit_id = request.GET.get('edit')

    if edit_id:
        try:
            edit_category = Category.objects.get(id=edit_id, user=request.user)
        except Category.DoesNotExist:
            messages.error(request, "Nategory not found")

    if request.method == 'POST':

        #  Add category
        if 'add_category' in request.POST:
            name = request.POST.get('name', '').strip()
            icon = request.POST.get('icon', 'fas fa-tag')
            color = request.POST.get('color', '').strip()
            description = request.POST.get('description', '').strip()

            if not name:
                messages.error(request, 'Category name is required.')
            elif Category.objects.filter(name=name, user=request.user).exists():
                messages.error(request, f"Category '{name}' already exists.")
            else:
                Category.objects.create(
                    user = request.user,
                    name = name,
                    icon = icon,
                    color = color,
                    description = description,

                )
                messages.success(request, 'Category added successfully.')
            return redirect('categories')


        
        # Edit category
        elif 'edit_category' in request.POST:
            category_id = request.POST.get('category_id')
            category = get_object_or_404(Category, id=category_id, user=request.user)

        
            name = request.POST.get('name', '').strip()
            icon = request.POST.get('icon', 'fas fa-tag')
            color = request.POST.get('color', '#3498db')
            description = request.POST.get('description', '').strip()

            if not name:
                messages.error(request, "Category name is required.")
            elif Category.objects.filter(name=name, user=request.user).exclude(id=category_id).exists():
                messages.error(request, f"Category '{name}' already exists.")
            else:
                category.name = name
                category.icon = icon
                category.color = color
                category.description = description
                category.save()
                messages.success(request, 'category updated successfully')
            return redirect('categories')
        
        # Delete Category
        elif 'delete_category' in request.POST:
            category_id = request.POST.get('category_id')

            category = get_object_or_404(Category, id=category_id, user=request.user)

            # Check if category has products
            product_count = category.product_set.count()
            if product_count > 0:
                messages.error(request, f'Cannot delete "{category.name}" - it has {product_count} product(s)!')
            else:
                category_name = category.name
                category.delete()
                messages.success(request, f"Category '{category_name}' deleted successfully.")
            return redirect('categories')
        
        
    context = {
        'product_list' : product_list,
        'categories' : categories_list,
        'edit_category' : edit_category,
    }
    return render(request, 'pages/categories.html', context)

@login_required
def barcode(request):
    product_list = Product.objects.filter(user=request.user).count()
    query = request.GET.get('scan')
    results = []
    if query:
        results = Product.objects.filter(
            barcode__icontains=query,
            user=request.user
        ).first()
    return render(request, 'pages/barcode_manager.html', {'product_list':product_list, 'results':results, 'query':query})

@login_required
def profile(request):
    product_list = Product.objects.filter(user=request.user).count()
    low_stock = Product.objects.filter(user=request.user, priority='low stock').count()
    out_of_stock = Product.objects.filter(user=request.user, priority='out of stock').count()

    dynamic ={
        'product_list' : product_list,
        'low_stock' : low_stock,
        'out_of_stock' : out_of_stock,
    }
    return render(request, 'pages/profile.html', dynamic)



@login_required
def search(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Product.objects.filter(
            title__icontains=query,
            user=request.user
        ).distinct()
    product_list = Product.objects.filter(user=request.user).count()
    return render(request, 'pages/search.html', {'product_list':product_list, 'query':query, 'results':results})
