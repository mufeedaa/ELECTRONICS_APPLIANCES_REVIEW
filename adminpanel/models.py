from django.contrib.auth.models import AbstractUser, AbstractBaseUser, Group, Permission, BaseUserManager
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings

# Create your models here.

class UserProfile(models.Model):

    # phone = models.CharField(max_length = 13, unique = True)
    profile_image = models.ImageField(upload_to = 'profile/')
    profile_description = models.TextField(max_length = 100)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)

    def __str__(self):
        return self.user.username

class Brand(models.Model):

    name = models.CharField(max_length = 100) 

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)  # Superuser must also have is_staff=True
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        return self.create_user(username, email, password, **extra_fields)




class User(AbstractBaseUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length = 13, unique = True)
    is_manager = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # Required for admin access
    is_user = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False) 
    is_admin = models.BooleanField(default=False)  # Required for superuser
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser    

        
class ManagerProfile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    groups = models.ManyToManyField(Group, related_name='manager_profiles', blank=True)

    profile_image = models.ImageField(upload_to = 'manager_profile/')
    phone = models.CharField(max_length = 13, unique = True)
    email = models.EmailField()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    author = models.ForeignKey(User, on_delete =  models.CASCADE )
    name = models.CharField(max_length=100) 

    class Meta:
        # Ensure each manager can have categories with unique names
        unique_together = ('author','name')

    def __str__(self):
        return self.name

class Appliance(models.Model):

    STATUS_CHOICES = (
        ('visible', 'Visible'),
        ('hidden', 'Hidden'),
    )

    name = models.CharField(max_length = 50)
    author = models.ForeignKey(User, on_delete =  models.CASCADE )
    brand = models.CharField(max_length = 50)
    image = models.ImageField(upload_to = 'appliances/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField( max_length = 200)
    price = models.DecimalField(max_digits = 8, decimal_places = 2, default = 0)
    discount = models.DecimalField(max_digits = 8, decimal_places = 2, default = 0)
    offer = models.DecimalField(max_digits = 3,decimal_places = 0, default = 0)
    release_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    status = models.CharField(max_length = 50, choices=STATUS_CHOICES, default='visible') 

    # def save(self, *args, **kwargs):
    #     # Automatically set author to the manager's first name
    #     if self.author and getattr(self.author, 'is_manager', False):
    #         self.author_name = self.added_by.first_name
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def average_rating(self):
        reviews = self.reviews.filter(status = 'visible')
        if reviews.exists():
            return sum(review.rating for review in reviews) / reviews.count()
        return 0   

class Review(models.Model):

    STATUS_CHOICES = (
        ('visible', 'Visible'),
        ('hidden', 'Hidden'),
    )

    review = models.TextField(max_length = 300)
    sample_image = models.ImageField(upload_to = 'review_images/',  blank=True, null=True)
    author = models.ForeignKey(User, on_delete = models.CASCADE) 
    appliance = models.ForeignKey(Appliance, on_delete = models.CASCADE, related_name='reviews')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True) 
    status = models.CharField(max_length = 50, choices = STATUS_CHOICES, default = 'visible')   
    rating = models.IntegerField(choices = [(i, i) for i in range(1,6)])
    likes = models.ManyToManyField(User, related_name='review_likes', blank=True)
    unlikes = models.ManyToManyField(User, related_name='review_unlikes', blank=True)

    class Meta:
        unique_together = ('author', 'appliance')  # Ensure a user can only review an appliance once
    
    def total_likes(self):
        return self.likes.count()

    def total_unlikes(self):
        return self.unlikes.count()

    def liked_users(self):
        return self.likes.all()

    def unliked_users(self):
        return self.unlikes.all()
        
    def __str__(self):
        return f'Review by {self.author.username} on {self.appliance.name} on {self.rating} Stars'

     


class Rating(models.Model):
    appliance = models.ForeignKey(Appliance, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating from 1 to 5
    created_at = models.DateTimeField(auto_now_add=True)

class ReviewLike(models.Model):

    review = models.ForeignKey(Review,  on_delete = models.CASCADE)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    liked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('review','author')  # Ensure a user can like a review only once

    def __str__(self):
        return f"{self.author.username} likes {self.review.id}"




