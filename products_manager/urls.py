from django.conf import settings
from django.urls import path
from .views import (home, manager_home, manager_sign_in, manager_register, add_category, edit_category, delete_category, category_list,
 add_product, edit_product, delete_product, product_list,
 product_view, hide_review, show_review, my_product, product_status, reset_password, forgot_password, profile_view, profile_edit, manager_sign_out)
from django.conf.urls.static import static


urlpatterns = [
    path('', home, name = 'home'),
    path('signin/', manager_sign_in, name = 'manager_login'),
    path('home/', manager_home, name = 'manager_home'),
    path('manager_register/', manager_register, name = 'manager_register'),
    path('addcategory/', add_category, name = 'manager_addcategory'),
    path('editcategory/<int:category_id>/', edit_category, name = 'manager_editcategory'),
    path('deletecategory/<int:category_id>/', delete_category, name = 'manager_deletecategory'),
    path('categorylist/', category_list, name = 'manager_categorylist'),
    path('addproduct/', add_product, name = 'manager_addproduct'),
    path('editproduct/<int:appliance_id>/', edit_product, name = 'manager_editproduct'),
    path('deleteproduct/<int:appliance_id>', delete_product, name = 'manager_deleteproduct'),
    path('productlist/', product_list, name = 'manager_productlist'),
    path('productview/<int:appliance_id>/', product_view, name = 'manager_productview'),
    path('hidereview/<int:review_id>/', hide_review, name = 'manager_hidereview'),
    path('showreview/<int:review_id>/', show_review, name = 'manager_showreview'),
    
    path('myproduct/', my_product, name = 'manager_myproduct'),
    path('productstatus/<int:appliance_id>', product_status, name = 'manager_productstatus'),
    path('resetpassword/', reset_password, name = 'manager_resetpassword'),
    path('forgotpassword/', forgot_password, name = 'manager_forgotpassword'),
    path('profileview/', profile_view, name = 'manager_viewprofile'),
    path('editprofile/', profile_edit , name = 'manager_editprofile'),
    path('signout/', manager_sign_out, name = 'manager_logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)