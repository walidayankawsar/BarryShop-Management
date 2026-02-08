from django import forms
from . models import Contact

class Msg_form(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'phone', 'msg']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input', 
                'placeholder': ' ', 
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'input', 
                'placeholder': ' ',
                'required': True
            }),
            'msg': forms.Textarea(attrs={
                'class': 'input', 
                'placeholder': ' ',
                'required': True
            }),
        }