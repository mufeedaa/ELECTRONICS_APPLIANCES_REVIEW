from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from adminpanel.models import UserProfile, User, Category, Appliance, Review
from products_manager.forms import CategoryForm, ApplianceForm
from django.contrib import messages
from .forms import ProfileEditForm, UserProfileForm, UserResetPasswordForm, ReviewForm, RatingForm, ApplianceSearchForm
from django.contrib.auth import logout
from django.db.models import Avg, Count
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
User = get_user_model()

# Create your views here.
@login_required(login_url='/404/')
def userhome(request):
    logged_user = request.user
    userprofile = get_object_or_404(UserProfile, user = logged_user)
    manager_count = User.objects.filter(is_manager = True, is_active = True).count()
    appliance_count = Appliance.objects.filter(status = 'visible' ).count()
    category_count = Category.objects.all().count()
    review_count = Review.objects.filter(status = 'visible').count()
    
   

    context = {
        'logged_user': logged_user,
        'userprofile': userprofile,'manager_count':manager_count,
        'appliance_count': appliance_count,
        'category_count': category_count,
        'review_count':review_count ,
    }
    return render(request, 'userpanel/user_home.html', context)

def logged_user_data(request):
    logged_user = request.user
    userprofile = get_object_or_404(UserProfile, user = logged_user)
    return logged_user, UserProfile

@login_required(login_url='/404/')
def product_list(request):
    
    logged_user = request.user
    userprofile = get_object_or_404(UserProfile, user = logged_user)

    appliances = Appliance.objects.filter(status = 'visible' ).order_by('-updated_at').annotate(average_rating=Avg('reviews__rating'))
    
    # using search
    form = ApplianceSearchForm(request.GET)

    if form.is_valid():
        keyword = form.cleaned_data.get('keyword')
            
        if keyword:
            # appliances = appliances.filter(
            #     Q(name__icontains=keyword) |
            #     Q(description__icontains=keyword) |
            #     Q(category__name__icontains=keyword) |
            #     Q(author__first_name__icontains=keyword)
            # )
            # Split the input into words
            search_terms = keyword.split()
            
            # Initialize queries for brand, category and price
            name_query = Q()
            author_query = Q()
            category_query = Q()
            price_query = Q()

            # Direct match check for appliance name
            exact_name_match = appliances.filter(name__icontains=keyword)
            if exact_name_match.exists():
                appliances = exact_name_match
            else:
                # Get all available categories
                available_categories = Category.objects.values_list('name', flat=True)

            
            # # Combine all filters
            # appliances = appliances.filter( (author_query & category_query) & price_query).distinct()

             # Loop through the terms to separate brand, category, and price
                for term in search_terms:
                    if term.isdigit():
                        # If the term is a number, treat it as a price filter
                        price_query = Q(price__lte=float(term))
                    elif term.lower() in [cat.lower() for cat in available_categories]:
                        # Check if term matches any known category
                        category_query |= Q(category__name__icontains=term)
                    else:
                        # Treat term as a brand (user's first name)
                        author_query |= Q(author__first_name__icontains=term)
                        name_query |= Q(name__icontains=term)
                # Combine filters (Category OR Brand) AND Price
                appliances = appliances.filter((author_query & category_query ) & (category_query | author_query | name_query )  & price_query).distinct()


    context = {
        'logged_user': logged_user,
        'userprofile': userprofile,
        'appliances': appliances,'form':form, 
        'star_range': range(1, 6), 
        
    }
    return render(request, 'userpanel/product_list.html', context)

@login_required(login_url='/404/')
def product_view(request, appliance_id):
    
    logged_user = request.user
    userprofile = get_object_or_404(UserProfile, user = logged_user)

    #appliance view
    appliance = get_object_or_404(Appliance, id = appliance_id)

    #view review
    reviews =  Review.objects.filter(appliance = appliance, status = 'visible')
    # review and rating count
    total_ratings = reviews.count()
    # average rating
    average_rating = appliance.average_rating()
    
   
    # Count each rating (1 to 5) and calculate percentage
    rating_counts = reviews.values('rating').annotate(count=Count('rating')).order_by('rating')
    rating_distribution = {i: 0 for i in range(1, 6)}  # Initialize with 0 for all ratings

    for entry in rating_counts:
        rating = entry['rating']
        count = entry['count']
        rating_distribution[rating] = (count / total_ratings) * 100

    # all reviews without logged user
    all_reviews = Review.objects.filter(appliance = appliance, status = 'visible').exclude(author = request.user).order_by('-created_at')

    total_reviews = all_reviews.count()
    # users review with logged user
    user_review = Review.objects.filter(appliance = appliance,author = request.user).first()
   
    # using search
      # using search
    
    if user_review:
        form  = None
        # message = "You have already reviewed this appliance."

    else:    

        #add review
        if request.method == 'POST':
            # if not user_review:  # Ensure the user can only post one review
            form = ReviewForm(request.POST, request.FILES)
            if form.is_valid() :
                
                review = form.save(commit = False)
                review.appliance = appliance
                review.author = request.user
                review.save()           

                messages.success(request, 'Your Review and Rating Added Successfully!!')
                return redirect('user_productview', appliance_id = appliance_id)
        else:
            # if not user_review:
            form = ReviewForm()  
            # message = None

     
    

    context = {
        'appliance': appliance, 'form':form,
        'all_reviews': all_reviews,
        'reviews':reviews,
        'user_review': user_review if user_review and user_review.status == 'visible' else None,
        'star_range': range(1, 6),  
        'logged_user': logged_user,
        'userprofile': userprofile,
        'average_rating': average_rating,
        # 'existing_reviews': existing_reviews,
        'total_ratings': total_ratings,
        'total_reviews': total_reviews,
        # 'rating_distribution': rating_distribution,
        # 'message': message,
        'form':form, 
      
    }            
    return render(request, 'userpanel/product_view.html', context)

def more_reviews(request, appliance_id):
    logged_user = request.user
    userprofile = get_object_or_404(UserProfile, user = logged_user)

    
    appliance = get_object_or_404(Appliance, id=appliance_id)
    #view review
    reviews =  Review.objects.filter(appliance = appliance, status= 'visible' )

    # all reviews without logged user
    all_reviews = Review.objects.filter(appliance = appliance, status = 'visible').exclude(author = request.user).order_by('-created_at')
    total_reviews = all_reviews.count()
    # review and rating count
    total_ratings = reviews.count()
    # average rating
    average_rating = appliance.average_rating()

   
        
    
    context = {
        'logged_user': logged_user,
        'userprofile': userprofile,
        'appliance': appliance,
        'reviews':reviews,
        'star_range': range(1, 6),  
        'total_ratings': total_ratings,
        'total_reviews': total_reviews,
        'all_reviews': all_reviews,
        'average_rating': average_rating,
       
    }
    return render(request, 'userpanel/more_reviews.html' ,context)


@login_required(login_url='/404/')
def review_edit(request, review_id):
    
    logged_user = request.user
    userprofile = get_object_or_404(UserProfile, user = logged_user)
    review = get_object_or_404(Review, id = review_id)
    appliance = get_object_or_404(Appliance, id = review.appliance.id)
    
    # all reviews without logged user
    all_reviews = Review.objects.filter(appliance = appliance, status = 'visible').exclude(author = request.user).order_by('-created_at')
    total_reviews = all_reviews.count()
    

    # average rating
    average_rating = appliance.average_rating()
    
    

    if request.method == 'POST':
        form = ReviewForm(request.POST,request.FILES , instance = review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Review Updated Successfully!')
            return redirect('user_productview', appliance_id = review.appliance.id)

        else:
          
            messages.error(request, 'The action failed') 
            return redirect('user_productview', appliance_id = review.appliance.id)

    else:
        form = ReviewForm(instance = review)



 
        
    context = {
        'logged_user': logged_user,
        'review':review, 'appliance':appliance,
        'all_reviews': all_reviews, 'userprofile': userprofile,
        'form': form,'star_range': range(1, 6), 
        'total_reviews':total_reviews,
        'average_rating':average_rating,
        'form': form,
       
    }               
    return render(request, 'userpanel/product_view.html', context)

@login_required(login_url='/404/')
def review_delete(request, review_id):
    logged_user = request.user
    review = get_object_or_404(Review, id = review_id, author = request.user)
    appliance_id = review.appliance.id
    review.delete()
    messages.success(request, 'Review and rating deleted successfully')
    return redirect('user_productview', appliance_id = appliance_id)   

def like_review(request, review_id):
    author = request.user
    
    review = get_object_or_404(Review, id = review_id)
   
    if request.user in review.likes.all():
        messages.warning(request, "You have already liked this review.")
    else:
        review.likes.add(request.user)
        messages.success(request, "Review liked successfully!")

    return redirect('user_morereview', appliance_id = review.appliance.id)

def unlike_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    author = request.user

    if request.user in review.likes.all():
        review.likes.remove(request.user)
        messages.success(request, "Review unliked successfully!")
    else:
        messages.warning(request, "You have not liked this review yet.")
    return redirect('user_morereview', appliance_id = review.appliance.id)

@login_required(login_url='/404/')
def manager_list(request):
    logged_user = request.user
    userprofile = get_object_or_404(UserProfile, user = logged_user)
    
    managers = User.objects.filter(is_manager = True)

    
           
    context = {
        'logged_user':logged_user,
        'userprofile':userprofile,'managers':managers,
        
    }
    return render(request, 'userpanel/manager_list.html', context)       

# appliance of selected manager
@login_required(login_url='/404/')
def appliance_list(request, user_id):
    logged_user = request.user
    userprofile = get_object_or_404(UserProfile, user = logged_user)
    
    author = get_object_or_404(User, id = user_id)
    appliances = Appliance.objects.filter(author = author)

   

    context = {
        'author': author,
        'appliances':appliances,
        'logged_user':logged_user,
        'userprofile':userprofile,
        
    }
    return render(request, 'userpanel/product_list.html', context)


@login_required(login_url='/404/')
def view_profile(request):
    logged_user = request.user
    userprofile = get_object_or_404(UserProfile, user = logged_user)

     # using search
    form = ApplianceSearchForm(request.GET)

    if form.is_valid():
        keyword = form.cleaned_data.get('keyword')
            
        if keyword:
            # Split the input into words
            search_terms = keyword.split()
            
            # Initialize queries for brand, category and price
            author_query = Q()
            category_query = Q()
            price_query = Q()

            # Loop through the terms to separate brand, category and price
            for term in search_terms:
                if term.isdigit():
                    # If the term is a number, treat it as a price filter
                    price_query = Q(price__lte=float(term))
                else:
                   # Check if term matches any brand (user's first name)
                    author_query |= Q(author__first_name__icontains=term)
                    # Check if term matches any category
                    category_query |= Q(category__name__icontains=term)

            # Combine all filters
            appliances = appliances.filter(author_query & category_query & price_query).distinct()
    
        
    context = {
        'logged_user': logged_user,
        'userprofile': userprofile,
        'form':form,
    }
    return render(request, 'userpanel/view_profile.html', context)

@login_required(login_url='/404/')
def edit_profile(request):
    

    logged_user = request.user
    userprofile = get_object_or_404(UserProfile, user = logged_user)
    
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        pro_form = UserProfileForm(request.POST,request.FILES, instance=request.user.userprofile)
        if form.is_valid() and pro_form.is_valid():
            form.save()
            pro_form.save()
            messages.success(request, 'Your profile has been updated!!')
            return redirect('user_viewprofile')  
    else:
        form = ProfileEditForm(instance=request.user)
        pro_form = UserProfileForm(instance=request.user.userprofile)




    context = {
        'form':form, 
        'pro_form':pro_form,
        'logged_user': logged_user,
        'userprofile': userprofile,
       
    }    

    return render(request, 'userpanel/edit_profile.html', context)

@login_required(login_url='/404/')
def reset_password(request):
    logged_user = request.user
    userprofile = get_object_or_404(UserProfile, user = logged_user)

    if request.method == 'POST':
        form = UserResetPasswordForm(user = request.user, data = request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request,'Your password has been updated seccessfully.')
            return redirect('site_login')
        else:
            errors = form.errors.as_json()
            print("Form errors:", errors)
            messages.error(request, 'Please correct the errors.')
    else:
        form = UserResetPasswordForm(user = request.user)  
   

    context = {
        'form':form,
        'logged_user': logged_user,
        'userprofile': userprofile,
        # 'appliances': appliances,'form':form,
    }
    return render(request, 'userpanel/reset_password.html', context)                    

def search_results(request):
    query = request.GET.get('query')  # Retrieve the search term from the URL query parameter
    if query:
        # Filter appliances where the name or category contains the search term (case-insensitive)
        appliances = Appliance.objects.filter(name__icontains=query) | Appliance.objects.filter(category__icontains=query)
    else:
        appliances = Appliance.objects.all()  # If no search term, display all appliances

    context = {
        'appliances': appliances,
        'query': query,
    }
    return render(request, 'userpanel/product_list.html', context)

@login_required(login_url='/404/')
def sign_out(request):
    logout(request)
    return redirect('site_home')   