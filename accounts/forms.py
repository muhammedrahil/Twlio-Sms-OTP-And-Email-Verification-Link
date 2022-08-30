from django import forms

from .models import User


class LoginUser(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'email','name':'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'password','name':'password'}))
    

class UserForm(forms.ModelForm):
    password= forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'enter a password'
    }))
    confrim_password= forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'enter a confrim password'
    }))
    class Meta:
        model=User
        fields=['email','phone_no','first_name','last_name','password']
        
    def clean(self):
        c=super(UserForm,self).clean()
        password = c.get('password')
        confrim_password =c.get('confrim_password')
        if password != confrim_password:
            raise forms.ValidationError('password does not match')