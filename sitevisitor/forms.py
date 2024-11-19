from django import forms
from adminpanel.models import User, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

class UserProfileForm(forms.ModelForm):
    # phone = forms.CharField(label = 'Phone:', required=True, widget = forms.TextInput(attrs={
    #     'class' : 'form-control',
    #     'placeholder' : 'Enter your phone number '
    # }))
    profile_image = forms.ImageField(label = 'Profile image:', required=True, widget = forms.ClearableFileInput(attrs={
        'class' : 'form-control'
       
    }))
    
    profile_description = forms.CharField(label = 'About:', required=True, widget = forms.Textarea(attrs={
        'class' : 'form-control',
        'placeholder' : 'Describe yourself '
    }))
    class Meta:
        model = UserProfile
        fields = [ 'profile_image', 'profile_description']


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label= 'First Name',required = True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your first name'
    }))
    last_name = forms.CharField(label= 'Last Name',required = True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your last name'
    }))
    email = forms.CharField(label= 'Email',required = True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email address'
    }))
    username = forms.CharField(label= 'Username',required = True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your username'
    }))
   
    password1 = forms.CharField(label= 'Password',required = True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your password'
    }))
    password2 = forms.CharField(label= 'Confirm Password',required = True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your confirm password'
    }))
    phone = forms.CharField(label = 'Phone:', required=True, widget = forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Enter your phone number '
    })) 
    # is_user = forms.BooleanField(required = True, label = 'Register as User' ) 
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username','password1', 'password2', 'phone']       


class LoginForm(forms.Form):
    username = forms.CharField(label = 'Username',max_length=100,required = True,
     widget = forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Enter your username'
    }))   
    password = forms.CharField(label = 'Password',max_length=100,required = True,
     widget = forms.PasswordInput(attrs={
        'class':'form-control', 
        'placeholder':'Enter your password'
    }))           


class SiteForgotPasswordForm(forms.Form):
    email = forms.CharField(label= 'Email',required = True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email address'
    }))
    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     # Check if any user exists with this email
    #     UserModel = get_user_model()
    #     if not UserModel.objects.filter(email=email).exists():
    #         raise forms.ValidationError("No user is associated with this email address.")
    #     return email
    class Meta:
        model = User
        fields = ['email']

    

class SiteResetPasswordForm(forms.Form):
    username = forms.CharField(label = 'Username',max_length=100,required = True,
     widget = forms.TextInput(attrs={
        'class':'form-control',
         'placeholder':'Enter your username'
    }))   
    password3 = forms.CharField(label = 'New Password',max_length=100,required = True,
     widget = forms.PasswordInput(attrs={
        'class':'form-control', 
        'placeholder':'Enter your new password'
    }))   
    password4 = forms.CharField(label = 'Confirm Password',max_length=100,required = True,
     widget = forms.PasswordInput(attrs={
        'class':'form-control', 
        'placeholder':'Confirm your password'
    }))   

    class Meta:
        fields = ['username', 'password3', 'password4']      

class SiteOtpForm(forms.Form):
    otp = forms.CharField(label='Enter Otp', max_length=6, min_length=6, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter 6 digit otp'
    }))    