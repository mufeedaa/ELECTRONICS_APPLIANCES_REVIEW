from django import forms
from adminpanel.models import Category, Appliance, User, ManagerProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import  PasswordChangeForm
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
User = get_user_model()

class CategoryForm(forms.ModelForm):
    name = forms.CharField(label= 'Category Name', widget=forms.TextInput(attrs={
        'Class': 'form-control',
        'placeholder': 'Enter the category name'
    }))
    class Meta:
        model = Category
        fields = ['name']

    


class ApplianceForm(forms.ModelForm):
    # logged_user = logged_user_data(request)
    # queryset=Category.objects.all() , queryset=Category.objects.filter(author = author)
    category = forms.ModelChoiceField(label= 'Category:', queryset=Category.objects.none(), required=True,  widget= forms.Select(attrs={
        'Class': 'form-control',
     }))
    name = forms.CharField(label = 'Model:', required=True, widget = forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Enter your appliance model '
    }))
    description = forms.CharField(label = 'Description:', required=True, widget = forms.Textarea(attrs={
        'class' : 'form-control',
        'placeholder' : 'Describe appliance content '
    }))
    image = forms.ImageField(label = 'Appliance image:', required=True, widget = forms.ClearableFileInput(attrs={
        'class' : 'form-control'
       
    }))
    # brand = forms.CharField(label = 'Brand:', required=True, widget = forms.TextInput(attrs={
    #     'Class': 'form-control',
    #     'placeholder': 'Enter your brand name '
    # }))
    price = forms.IntegerField(label = 'Price:', required=True, widget = forms.NumberInput(attrs={
        'Class': 'form-control',
        'placeholder': ' Enter appliance price '
    }))
    offer = forms.IntegerField(label = 'Offer:', required=True, widget = forms.NumberInput(attrs={
        'Class': 'form-control',
        'placeholder': ' Enter appliance offer '
    }))
    discount =  forms.IntegerField(label = 'Discount Price:', required=True, widget = forms.NumberInput(attrs={
        'Class': 'form-control',
        'placeholder': ' Enter appliance discount price '
    }))
    release_date = forms.DateField(label = 'Release Date:', required=True, widget = forms.DateInput(attrs={
        'type': 'date',
        'Class': 'form-control',
        'placeholder': 'Enter the release date'

    }))
    class Meta:
        model = Appliance
        fields = ['category', 'name','image','description','price','offer', 'discount','release_date']

    # Custom initialization method to accept the logged-in user
    def __init__(self, *args, **kwargs):
        author = kwargs.pop('author', None)  # Pop the user parameter from kwargs
        super(ApplianceForm, self).__init__(*args, **kwargs)
        
        # Filter the categories based on the user's company
        if author:
            self.fields['category'].queryset = Category.objects.filter(author = author)





class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label= 'Brand Name',required = True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your brand name'
    }))
    
    email = forms.CharField(label= 'Email',required = True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your brand email address'
    }))
    username = forms.CharField(label= 'Username',required = True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your brand username'
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
        'placeholder' : 'Enter your brand phone number '
    })) 
    is_manager = forms.BooleanField(required = True, label = 'Register as Manager' ) 
    class Meta:
        model = User
        fields = ['first_name', 'username','email','password1', 'password2','phone', 'is_manager' ]           


    # def save(self, commit = True):
    #     user = super().save(commit = False)
    #     user.is_manager = True
    #     if commit:
    #         user.save()
    #     return user  
    def clean_is_manager(self):
        is_manager = self.cleaned_data.get("is_manager")
        if not is_manager:
            raise forms.ValidationError("You must register as a manager.")
        return is_manager  

class ManagerProfileForm(forms.ModelForm):
    profile_image = forms.ImageField(label = 'Profile image:', required=True, widget = forms.ClearableFileInput(attrs={
        'class' : 'form-control'
       
    }))
    model = ManagerProfile
    fields = ['profile_image']

class LoginForm(AuthenticationForm):
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
    def confirm_login_allowed(self, user):
        if not user.is_manager:
            raise forms.ValidationError("Only managers can log in here.")
    # class Meta:
    #     model = ManagerProfile
    #     fields = ['username', 'password']


class ManagerResetPasswordForm(PasswordChangeForm):
    def __int__(self, is_manager, *args, **kwargs):
        super().__int__(is_manager, *args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        fields = ['old_password2', 'new_password5', 'new_password6']        

class ManagerForgotPasswordForm(forms.ModelForm):
    email = forms.CharField(label= 'Email',required = True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email address'
    }))
    def clean_email(self):
        email = self.cleaned_data['email']
        # Check if any user exists with this email
        UserModel = get_user_model()
        if not UserModel.objects.filter(email=email).exists():
            raise forms.ValidationError("No user is associated with this email address.")
        return email
    class Meta:
        model = User
        fields = ['email']