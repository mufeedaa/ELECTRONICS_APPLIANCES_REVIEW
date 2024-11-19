from django.contrib import admin
from .models import UserProfile, Category, Appliance, Review, Rating, ReviewLike, User, ManagerProfile

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Appliance)
admin.site.register(Review)
admin.site.register(Rating)
admin.site.register(ReviewLike)
admin.site.register(User)
admin.site.register(ManagerProfile)