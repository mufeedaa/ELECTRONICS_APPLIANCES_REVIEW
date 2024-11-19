from django.conf import settings
from django.shortcuts import render, redirect 
from adminpanel.models import UserProfile,  Appliance
from .forms import UserProfileForm, RegisterForm, LoginForm, SiteForgotPasswordForm, SiteResetPasswordForm, SiteOtpForm
from products_manager.forms import ApplianceForm
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

import random


# Create your views here.

def sitehome(request):
    appliances = Appliance.objects.filter(status = 'visible' )
    return render(request, 'sitevisitor/site_home.html', {'appliances':appliances})

def logged_user_data(request):
    logged_user = request.user
    userprofile = get_object_or_404(UserProfile, user = logged_user)
    return logged_user, UserProfile

def sign_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request,user)
                messages.success(request,'You Have Successfully login!!!WELCOME BACK!!')
                return redirect('user_home')
            else:
                messages.error(request, 'Invalid Usename or Password!!')
                return redirect('site_login')    

    else:
        form = LoginForm() 
    return render(request, 'sitevisitor/login.html', {'form': form})  

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        pro_form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid() and pro_form.is_valid():
            user = form.save()
            user_profile = pro_form.save(commit = False)
            user_profile.user = user
            user_profile.save()
            
            messages.success(request,'You Have Registered Successfully!!!')
            #  welcome email using Celery
            
            return redirect('site_login')
    else:
        form = RegisterForm()
        pro_form = UserProfileForm

    return render(request, 'sitevisitor/register.html', {'form': form, 'pro_form': pro_form})    

def generate_otp():
    return random.randint(100000, 999999)

def forgot_password(request):
    if request.method == 'POST':
        form = SiteForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email = email).exists():

                otp = generate_otp()
                request.session['otp'] = otp
                request.session['email'] = email

                request.session['otp_expiry'] = (timezone.now() + timezone.timedelta(minutes=2)).isoformat()
                
                messages.success(request, 'Instructions to reset your password.')
                return redirect('site_otp')
            else:
                messages.error(request,'This email id does not exist!!')
                return redirect('site_forgotpassword')

    else:
        form = SiteForgotPasswordForm()   
    return render(request, 'sitevisitor/forgot_password.html', {'form':form})    

def reset_password(request):
    if request.method == 'POST':
        form = SiteResetPasswordForm( request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password3 = form.cleaned_data.get('password3')
            password4 = form.cleaned_data.get('password4')

            if password3 != password4:
                form.add_error('password4', 'Passwords do not match.')
            else:
                user = User.objects.filter(username = username).first()
                if user:
                    user.set_password(password3)

                    user.save()
                    messages.success(request,'Your password has been updated successfully.')
                    return redirect('site_login')
                else:
                    form.add_error('username', 'User does not exist.')
            
        else:
            messages.error(request, 'Please correct the errors.')
    else:        
        form = SiteResetPasswordForm()   
    return render(request, 'sitevisitor/reset_password.html', {'form':form})    

def otp(request):
    if request.method == 'POST':
        form = SiteOtpForm(request.POST)
        if form.is_valid():

            input_otp = form.cleaned_data['otp']
           
            otp = request.session.get('otp')
            otp_expiry = request.session.get('otp_expiry')

            email = request.session.get('email')
            if input_otp and otp  ==  otp :
                # expiry_time = timezone.datetime.fromisoformat(otp_expiry)
                
                # if timezone.now() <= expiry_time:
                
               
                messages.success(request, 'OTP verified successfully..')
                return redirect('site_resetpassword')
            # else:
            #     messages.error(request, 'OTP has expired.')
    
            else:
                messages.error(request, 'Invalid OTP. please try again..')
                return redirect('site_otp')
    else:
        form = SiteOtpForm()  
    return render(request, 'sitevisitor/otp.html', {'form':form})    

def error_page(request):
    return render(request,'sitevisitor/404.html')    