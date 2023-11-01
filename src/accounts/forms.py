from .models import AdminUser
from django import forms 
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordResetForm , SetPasswordForm, PasswordChangeForm 

class UserRegistration(UserCreationForm):
    password1 = forms.CharField(widget= forms.PasswordInput(attrs={'class':'form-control','placeholder': 'Password'}))
    password2 = forms.CharField(widget= forms.PasswordInput(attrs={'class':'form-control','placeholder': 'Confirm Password'}))
    class Meta:
        model = AdminUser 
        fields = ['username','first_name', 'last_name', 'email', 'mobile_number', 'address'] 
        widgets = {'username':forms.TextInput(attrs={'class':'form-control','placeholder': 'Username'}),
                    'first_name':forms.TextInput(attrs={'class':'form-control','placeholder': 'First Name'}),
                    'last_name':forms.TextInput(attrs={'class':'form-control','placeholder': 'Last Name'}),
                    'email':forms.EmailInput(attrs={'class':'form-control','placeholder': 'Email'}),
                    'mobile_number':forms.NumberInput(attrs={'class':'form-control','placeholder': 'Mobile number', 'type':'tel'}),
                    'address':forms.TextInput(attrs={'class':'form-control','placeholder': 'Address'}),
                }
   
class LoginFormAuthentication(AuthenticationForm):
    username = UsernameField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Username',"autofocus": True}))
    password = forms.CharField(label='',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder': 'password'}))

class PasswordReset(PasswordResetForm):
    email = forms.CharField(label='', max_length=254,widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter Username or Email',"autocomplete": "email"}),
    )
     
class PasswordChangeForm(PasswordChangeForm, SetPasswordForm):
    old_password = forms.CharField(label="",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder': 'Existing password',"autocomplete": "current-password", "autofocus": True} ))
    new_password1 = forms.CharField(label="",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder': 'New password',"autocomplete": "new-password"}))
    new_password2 = forms.CharField(label="",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder': 'Confirm password',"autocomplete": "new-password"}))


