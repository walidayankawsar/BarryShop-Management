from django.shortcuts import render, redirect
from .forms import Msg_form
from .models import Contact
from django.contrib import messages

# Create your views here.

def message(request):
    if request.method == 'POST':
        form = Msg_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Messages sent Successfully')
            return redirect('contact')
    return render(request, 'contact.html')