from django.shortcuts import render, redirect, get_object_or_404
from adminpanel.models import User , Category, Appliance, Review
from .forms import  RegisterForm, ManagerProfileForm, LoginForm ,  CategoryForm, ApplianceForm, ManagerResetPasswordForm, ManagerForgotPasswordForm
from userpanel.forms import ReviewForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count
User = get_user_model()

# Create your views here.

def home(request):
    return render(request, 'products_manager/home.html')


# def is_manager(user):
#     return user.is_manager

def is_manager(user):
    """Check if the user has the is_manager attribute set to True."""
    return user.is_authenticated and getattr(user, 'is_manager', False)    

@login_required(login_url='/404/')
def manager_home(request):
    appliance_count = Appliance.objects.filter(author = request.user).count()
    category_count = Category.objects.filter(author = request.user).count()
    context = {
        'appliance_count':appliance_count,
        'category_count': category_count
    }
    return render(request, 'products_manager/manager_home.html', context )



def manager_sign_in(request):
    if request.method == 'POST':
        form = LoginForm(request, data = request.POST)
        if form.is_valid():
            user = form.get_user()
            # if user.is_manager:
            login(request, user)
            messages.success(request,'You Have Successfully Login! WELCOME BACK!!!')
            return redirect('manager_home')
        else:
            messages.error(request, 'Invalid Usename or Password!!')
            return redirect('manager_login') 
    else:
        form = LoginForm()  
    return render(request, 'products_manager/manager_login.html', {'form': form})




# def manager_register(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         manpro_form = ManagerProfileForm(request.POST, request.FILES)
#         if form.is_valid() and manpro_form.is_valid():
#             user = form.save()
#             manager_profile = manpro_form.save(commit = False)
#             manager_profile.user = user
#             manager_profile.save()
#             messages.success(request,'Successfully registered')
#             return redirect('manager_login')
#     else:
#         form = RegisterForm()
#         manpro_form = ManagerProfileForm()
#     return render(request, 'products_manager/manager_register.html', {'form': form, 'manpro_form':manpro_form})


def manager_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            login(request, user)
            messages.success(request,'You Have Successfully Registered!!!')
            return redirect('manager_login')  # Redirect to sign-in page after signup
    else:
        form = RegisterForm()
    return render(request, 'products_manager/manager_register.html', {'form': form})

@login_required(login_url='/404/')
def add_category(request):
    if not request.user.is_authenticated or not getattr(request.user, 'is_manager', False):
        return HttpResponseForbidden("Only managers can add appliances.")

    # logged_user = logged_user_data(request)
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit = False)
            # category.user = logged_user
            category.author = request.user
            category.save()
            messages.success(request, 'New category is created!!')
            return redirect('manager_categorylist')
    else:
        form = CategoryForm()
    return render(request, 'products_manager/add_category.html', {'form': form})

@login_required(login_url='/404/')
def edit_category(request, category_id):
    category = get_object_or_404(Category, id = category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance = category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!!!')
            return redirect('manager_categorylist')
    else:
        form = CategoryForm(instance = category)
    return render(request, 'products_manager/edit_category.html', {'form': form})

@login_required(login_url='/404/')
def delete_category(request, category_id):
    category = get_object_or_404(Category, id = category_id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully')
    return redirect('manager_categorylist')
    
@login_required(login_url='/404/')
def category_list(request):
    logged_user = request.user
    categories = Category.objects.all().order_by('-id')
    return render(request, 'products_manager/category_list.html', {'categories': categories, 'logged_user':logged_user})


@login_required(login_url='/404/')
def add_product(request):
    author = request.user  # Define the logged_user as the current user

    # Ensure only managers can access this view
    if not request.user.is_authenticated or not getattr(request.user, 'is_manager', False):
        return HttpResponseForbidden("Only managers can add appliances.")

    # logged_user = logged_user_data(request)
    if request.method == 'POST':
        form = ApplianceForm(request.POST, request.FILES, author = author)
        if form.is_valid():
            appliance = form.save(commit = False)
            # appliance.user = logged_user
            appliance.author = request.user
            appliance.save()
            messages.success(request, 'New Product added successfully')
            return redirect('manager_myproduct')
    else:
        form = ApplianceForm(author = author) 

    context = {
        # 'logged_user':logged_user,
        'form':form,
        'author' : author,
        # 'user_company': user_company,
    }       

    return render(request, 'products_manager/add_product.html', context)

@login_required(login_url='/404/')
def edit_product(request, appliance_id):
    author = request.user 
    appliance = get_object_or_404(Appliance, id = appliance_id)

    if request.method == 'POST':
        form = ApplianceForm(request.POST, request.FILES, instance = appliance, author = author )
        if form.is_valid():
            form.save()
            messages.success(request, 'Appliance details updated Successfully!!')
            return redirect('manager_myproduct')
    else:
        form = ApplianceForm(instance = appliance, author = author)     

    context = {
        'appliance':appliance,
        'form':form,
        'author': author
    }       
    return render(request, 'products_manager/edit_product.html', context)    

@login_required(login_url='/404/')
def delete_product(request, appliance_id):
    author = request.user
    appliance = get_object_or_404(Appliance, id = appliance_id, author = request.user)
    appliance.delete()
    messages.success(request, 'Appliance deleted successfully!')
    return redirect('manager_myproduct')

    context = { 
        'author':author,
        'appliance':appliance

    }
    return render(request, 'products_manager/product_list.html', context)    

@login_required(login_url='/404/')
def product_list(request):
    
    # if not request.user.is_authenticated or not getattr(request.user, 'is_manager', False):
    #     return HttpResponseForbidden("Only managers can add appliances.")

    # author = request.user
    appliances = Appliance.objects.filter(status = 'visible' ).order_by('-updated_at').annotate(average_rating=Avg('reviews__rating'))
    return render(request, 'products_manager/product_list.html', {'appliances': appliances, 'star_range': range(1, 6) })

@login_required(login_url='/404/')
def product_view(request, appliance_id):
    logged_user = request.user

    # appliance view
    appliance = get_object_or_404(Appliance, id = appliance_id)

    # view review
    reviews = Review.objects.filter(appliance = appliance)

    # review and rating count
    total_ratings = reviews.count()
    # average rating
    average_rating = appliance.average_rating()


    context = {
        'total_ratings': total_ratings,
        'average_rating': average_rating,
        'appliance': appliance, 
        'reviews':reviews,
        'star_range': range(1, 6), 
    }
    return render(request, 'products_manager/product_view.html', context)

@login_required(login_url='/404/')
def my_product(request):
    logged_user = request.user
    appliances = Appliance.objects.filter(author = request.user).order_by('-updated_at')
    return render(request, 'products_manager/my_product.html', {'appliances': appliances, 'logged_user':logged_user})

@login_required(login_url='/404/')
def product_status(request, appliance_id):
    appliance = get_object_or_404(Appliance, id = appliance_id)

    #  the status between 'hidden' and 'publish'
    if appliance.status == 'hidden':
        appliance.status = 'visible'
    else:
        appliance.status = 'hidden'
    
    # Save the appliane
    appliance.save()
    
    # Redirect to the appliance list or any other page
    return redirect('manager_myproduct')

def hide_review(request, review_id):
    review = get_object_or_404(Review, id = review_id)
    review.status = 'Hidden'
    review.save()
    appliance_id = review.appliance.id
    return redirect('manager_productview', appliance_id = appliance_id)

def show_review(request, review_id):
    review = get_object_or_404(Review, id = review_id)
    review.status = 'Visible'
    review.save()
    appliance_id = review.appliance.id
    return redirect('manager_productview', appliance_id = appliance_id)


@login_required(login_url='/404/')
def reset_password(request):
    if request.method == 'POST':
        form = ManagerResetPasswordForm(user = request.user, data = request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Your password has been updated seccessfully.')
            return redirect('manager_login')
        else:
            messages.error(request, 'Please correct the errors.')
    else:
        form = ManagerResetPasswordForm(user = request.user)  

    return render(request, 'products_manager/reset_password.html', {'form':form})            


def forgot_password(request):
    if request.method == 'POST':
        form = ManagerForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email = email).exists():
                messages.success(request, 'Instructions to reset your password.')
                return redirect('site_otp')
            else:
                messages.error(request,'This email id does not exist!!')
                return redirect('site_forgotpassword')

    else:
        form = ManagerForgotPasswordForm() 
    return render(request, 'products_manager/forgot_password.html', {'form':form})

@login_required(login_url='/404/')
def profile_view(request):
    if request.user.is_superuser:
        return HttpResponseForbidden("Superusers cannot access this page.")
    
    user = request.user
    # user = get_object_or_404(User, user = logged_user)
    context = {
        'user': user
        # 'user': user
    }
    return render(request, 'products_manager/view_profile.html', context)

@login_required(login_url='/404/')
def profile_edit(request):
    return render(request, 'products_manager/edit_profile.html')

def manager_sign_out(request):
    logout(request)
    return redirect('home')
     