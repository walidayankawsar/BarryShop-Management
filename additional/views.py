from django.shortcuts import render, redirect
from .forms import Msg_form
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def message(request):
    if request.method == 'POST':
        form = Msg_form(request.POST)
        if form.is_valid():
            mail = form.save()
            messages.success(request, 'Your Messages sent Successfully')
        
            # now message will be sent in gmail
            subject = "BarryShop Message"
            message = f"""
                Name: {mail.name}
                Phone: {mail.phone}
                Message: {mail.msg}
            """

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
        else:
            messages.error(request,'Your Messages fialed to send')
    else:
        form = Msg_form()
        return redirect('contact')

    return render(request, 'contact.html')