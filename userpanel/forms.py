from django import forms
from adminpanel.models import UserProfile,Category, Review, Rating
from django.contrib.auth.models import User
from django.contrib.auth.forms import  PasswordChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
User = get_user_model()


class ProfileEditForm(forms.ModelForm):
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
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly'  # Set the readonly attribute
    }))
    phone = forms.CharField(label = 'Phone:', required=True, widget = forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Enter your phone number '
    }))
   
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username','phone']
        

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


class UserResetPasswordForm(forms.Form):
    
    """
    A custom password change form for the userpanel, using unique field names
    to avoid conflicts with the adminpanel.
    """
    current_password = forms.CharField(
        label='Current Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Current Password'
        }),
        strip=False,
    )
    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter New Password'
        }),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    confirm_new_password = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm New Password'
        }),
        strip=False,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.user.check_password(current_password):
            raise forms.ValidationError("The current password is incorrect.")
        return current_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')

        if new_password and confirm_new_password:
            if new_password != confirm_new_password:
                raise forms.ValidationError("The new passwords do not match.")
        
        # Validate the new password against Django's validators
        password_validation.validate_password(new_password, self.user)
        return cleaned_data

    def save(self, commit=True):
        new_password = self.cleaned_data['new_password']
        self.user.set_password(new_password)
        if commit:
            self.user.save()
        return self.user
        
   


class ReviewForm(forms.ModelForm):
    sample_image = forms.ImageField( required = True, widget = forms.ClearableFileInput(attrs = {
        'class' : 'form-control', 
    }))
    review = forms.CharField(max_length = 200, required = True,
       widget = forms.Textarea(attrs = {
        'class': 'form-control',
        'placeholder' : 'Post your reviews here......'
    }))
    # rating = (widget = forms.RadioSelect(choices - [(i, f"{i} Stars ") for i in range(1, 6)], 
    # label="Rate this appliance". required=True))
    
    class Meta:
        model = Review
        fields = ['sample_image', 'review', 'rating']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f"{i} star_range") for i in range(1, 6)]),
        }

class RatingForm(forms.ModelForm):

    class Meta:
        model = Rating
        fields = ['rating']        


class ApplianceSearchForm(forms.Form):
    keyword = forms.CharField(max_length=200, required=False, 
    label="Search", widget=forms.TextInput(attrs={'placeholder': 'Search here... '})
    )
    