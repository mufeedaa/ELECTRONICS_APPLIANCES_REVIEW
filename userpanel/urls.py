from django.conf import settings
from django.urls import path
from .views import ( userhome, product_list, product_view, review_edit, review_delete, 
       more_reviews, like_review, unlike_review, manager_list, appliance_list, view_profile, edit_profile,
        search_results, reset_password, sign_out )
from django.conf.urls.static import static

urlpatterns = [
    path('', userhome, name = 'user_home'),
    path('productlist/', product_list, name = 'user_productlist'),
    path('productview/<int:appliance_id>/', product_view, name = 'user_productview'),
    path('morereview/<int:appliance_id>/', more_reviews, name = 'user_morereview'),
    path('reviewedit/<int:review_id>/', review_edit, name = 'user_reviewedit'),
    path('reviewdelete/<int:review_id>/', review_delete, name = 'user_reviewdelete'),
    path('likereview/<int:review_id>/like/', like_review, name = 'user_likereview'),
    path('unlikereview/<int:review_id>/unlike/', unlike_review, name = 'user_unlikereview'),
    path('managerlist/', manager_list, name = 'user_managerlist'),
    path('appliancelist/<int:user_id>/', appliance_list, name = 'user_appliancelist'),
    path('viewprofile/', view_profile, name = 'user_viewprofile'),
    path('editprofile/', edit_profile, name = 'user_editprofile'),
    path('resetpassword/', reset_password, name = 'user_resetpassword'),
    path('searchresult/', search_results, name = 'user_searchresult'),
    path('logout/', sign_out, name = 'user_logout')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)