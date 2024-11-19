from django.shortcuts import render, redirect, get_object_or_404
from .models import  Appliance, Category, UserProfile, User, Review
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import AdminResetPasswordForm, LoginForm, ApplianceForm, CategoryForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from django.db.models import Avg, Count
User = get_user_model()


# Create your views here.

@login_required(login_url='/404/')
def adminhome(request):
    logged_user = request.user
    user_count = User.objects.filter(is_staff = False, is_manager = False).count()
    manager_count = User.objects.filter(is_manager = True).count()
    appliance_count = Appliance.objects.all().count()
    category_count = Category.objects.all().count()
    
    context = { 
    'logged_user':logged_user,
    'user_count':user_count,
    'manager_count':manager_count,
    'appliance_count': appliance_count,
    'category_count': category_count,
    }

    return render(request, 'adminpanel/admin_home.html', context)

def is_staff(user):
    return user.is_staff

def admin_sign_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username = username, password = password)
            if user is not None and user.is_staff:
                logout(request)
                login(request,user)
                messages.success(request,'You Have Successfully Login! WELCOME BACK!!!')
                return redirect('admin_home')
            else:
                messages.error(request, 'Invalid Usename or Password!!')
                return redirect('admin_login')    

    else:
        form = LoginForm() 
    return render(request, 'adminpanel/admin_login.html', {'form': form})
    
@login_required(login_url='/404/')    
def user_list(request):
    
    users = User.objects.filter(is_staff = False, is_manager = False)
   
    
    userprofiles = UserProfile.objects.all()
    context = {
        'users': users,
        'userprofile': userprofiles,
       
    }
    return render(request, 'adminpanel/user_list.html', context)

@login_required(login_url='/404/')
def user_view(request, user_id):
    user = get_object_or_404(User, id = user_id)
    userprofile = user.userprofile
    context = {
        'user':user,
        'userprofile':userprofile,
    }
    return render(request, 'adminpanel/user_view.html', context)    

def user_status(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if user.is_active:
        user.is_active = False
        messages.success(request, f'User {user.username} has been deactivated.')
        
    else:
        user.is_active = True
        messages.success(request, f'User {user.username} has been activated.')

        

    user.save()
    return redirect('admin_userlist')

@login_required(login_url='/404/')
def product_list(request):
    appliances = Appliance.objects.filter(status = 'visible' ).order_by('-updated_at').annotate(average_rating=Avg('reviews__rating'))
    return render(request, 'adminpanel/product_list.html', {'appliances':appliances, 'star_range': range(1, 6), }) 

@login_required(login_url='/404/')
def product_view(request, appliance_id):
      # appliance view
    appliance = get_object_or_404(Appliance, id = appliance_id)
     # view review
    reviews = Review.objects.filter(appliance = appliance)
    total_reviews = reviews.count()
    # review and rating count
    total_ratings = reviews.count()
    # average rating
    average_rating = appliance.average_rating()



    context = {
        'appliance': appliance, 'reviews':reviews,
        'star_range': range(1, 6), 
        'total_ratings': total_ratings,
        'average_rating': average_rating,
    }
    return render(request, 'adminpanel/product_view.html', context)       

def hide_review(request, review_id):
    review = get_object_or_404(Review, id = review_id)
    review.status = 'Hidden'
    review.save()
    appliance_id = review.appliance.id
    return redirect('admin_productview', appliance_id = appliance_id)

def show_review(request, review_id):
    review = get_object_or_404(Review, id = review_id)
    review.status = 'Visible'
    review.save()
    appliance_id = review.appliance.id
    return redirect('admin_productview', appliance_id = appliance_id)

# category of selected manager
@login_required(login_url='/404/')
def category_list(request, user_id):
    user = get_object_or_404(User, id = user_id)
    categories = Category.objects.filter(author = user)
    return render(request, 'adminpanel/manager_category_list.html', {'user':user, 'categories':categories})

#appliance of selected category
@login_required(login_url='/404/')
def category_appliance(request, category_id):
    category = get_object_or_404(Category, id = category_id)
    appliances = Appliance.objects.filter(category = category)
    context = {
        'category': category,
        'appliances': appliances
    }
    return render(request, 'adminpanel/product_list.html', context)

# appliance of selected manager
@login_required(login_url='/404/')
def appliance_list(request, user_id):
    user = get_object_or_404(User, id = user_id)
    appliances = Appliance.objects.filter(author = user)
    context = {
        'user': user,
        'appliances':appliances,
    }
    return render(request, 'adminpanel/product_list.html', context)

@login_required(login_url='/404/')
def manager_list(request):
    
    managers = User.objects.filter(is_manager = True)
    return render(request, 'adminpanel/manager_list.html', {'managers':managers})       

def manager_status(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if user.is_active:
        user.is_active = False
        messages.success(request, f'User {user.username} has been deactivated.')
       
    else:
        user.is_active = True
        messages.success(request, f'User {user.username} has been activated.')
   

    user.save()
    return redirect('admin_managerlist')



@login_required(login_url='/404/')
def reset_password(request):
    
    if request.method == 'POST':
        form = AdminResetPasswordForm(user = request.user, data = request.POST )
        if form.is_valid():
            form.save()
            # update_session_auth_hash(request, request.user)  
            messages.success(request,'Your password has been updated seccessfully.')
            return redirect('admin_login')
        else:
            # Display form errors for debugging
            errors = form.errors.as_json()
            print("Form errors:", errors)
            messages.error(request, 'Please correct the errors.')
    else:
        form = AdminResetPasswordForm(user = request.user) 

   
    return render(request, 'adminpanel/reset_password.html', {'form':form})    

@login_required(login_url='/404/')
def admin_sign_out(request):    
    logout(request)
    return redirect('admin_login')