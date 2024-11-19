from django.conf import settings
from django.urls import path
from .views import ( adminhome, admin_sign_in, user_list, user_view, product_list, product_view, manager_list,
    hide_review, show_review, user_status, category_list, manager_status,category_appliance, appliance_list, reset_password, admin_sign_out )
from django.conf.urls.static import static

urlpatterns = [
    path('', admin_sign_in, name = 'admin_login'),
    path('adminhome/', adminhome, name = 'admin_home'),
    path('userlist/', user_list, name = 'admin_userlist'),
    path('userview/<int:user_id>/', user_view, name = 'admin_userview'),
    path('userstatus/<int:user_id>/', user_status, name = 'admin_userstatus'),
    path('productlist/', product_list, name = 'admin_productlist'),
    path('productview/<int:appliance_id>/', product_view, name = 'admin_productview'),
    path('hidereview/<int:review_id>/', hide_review, name = 'admin_hidereview'),
    path('showreview/<int:review_id>/', show_review, name = 'admin_showreview'),
    path('managerlist/', manager_list, name = 'admin_managerlist'),
    path('managerstatus/<int:user_id>/', manager_status, name = 'admin_managerstatus'),
    path('categorylist/<int:user_id>/', category_list, name = 'admin_categorylist'),
    path('appliancelist/<int:user_id>/', appliance_list, name = 'admin_appliancelist'),
    path('categoryappliance/<int:category_id>/', category_appliance, name = 'admin_categoryappliance'),
    path('resetpassword/', reset_password, name = 'admin_resetpassword'),
    path('signout/', admin_sign_out, name = 'admin_logout'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)