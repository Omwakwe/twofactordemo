from django import forms
from accounts.models import *

class SignupForm(forms.ModelForm):
    user_name = forms.CharField(widget=forms.TextInput(attrs={'class':"form-control input-sm", }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':"form-control input-sm", }))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class':"form-control input-sm", }))
    first_name = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':"form-control input-sm", }))
    second_name = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':"form-control input-sm", }))
    last_name = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':"form-control input-sm", }))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': "form-control input-sm",}))

    class Meta:
        model = User
        fields = ('user_name','first_name','second_name','last_name'\
        			,'email', 'password','password_confirm',)

class LoginForm(forms.Form):
    user_name = forms.CharField(widget=forms.TextInput(attrs={'class':"form-control input-sm", }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':"form-control input-sm", }))

    class Meta:
        fields = ('user_name', 'password',)

class ProfileForm(forms.ModelForm):
    user_name = forms.CharField(widget=forms.TextInput(attrs={'class':"form-control input-sm", }))
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':"form-control input-sm", }))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':"form-control input-sm", }))
    first_name = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':"form-control input-sm", }))
    second_name = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':"form-control input-sm", }))
    last_name = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':"form-control input-sm", }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': "form-control input-sm",}))

    class Meta:
        model = User
        fields = ('user_name','first_name','second_name','last_name'\
                    ,'email', 'old_password','new_password',)