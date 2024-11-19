from django import forms
from .models import Category, Appliance
from django.contrib.auth.models import User
from django.contrib.auth.forms import  PasswordChangeForm
from django.contrib.auth import get_user_model
User = get_user_model()


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

class AdminResetPasswordForm(PasswordChangeForm):
    def __int__(self, user, *args, **kwargs):
        super().__int__(user, *args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    old_password = forms.CharField(
        label='Current Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Current Password'
        }))
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter New Password'
        })) 
    new_password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Confirm Password'
        }))       
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
    

class CategoryForm(forms.ModelForm):
    name = forms.CharField(label= 'Category Name', widget=forms.TextInput(attrs={
        'Class': 'form-control',
        'placeholder': 'Enter the category name'
    }))
    class Meta:
        model = Category
        fields = ['name']

        
class ApplianceForm(forms.ModelForm):
    category = forms.ModelChoiceField(label= 'Category:', required=True, queryset=Category.objects.all(), widget= forms.Select(attrs={
        'Class': 'form-control',
     }))
    name = forms.CharField(label = 'Appliance Name:', required=True, widget = forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Enter your appliance name '
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
    release_date = forms.DateField(label = 'Release Date:', required=True, widget = forms.DateInput(attrs={
        'type': 'date',
        'Class': 'form-control',
        'placeholder': 'Enter the release date'

    }))
    class Meta:
        model = Appliance
        fields = ['category', 'name','image','description','price','release_date']
