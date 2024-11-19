from django.conf import settings
from django.urls import path
from .views import sitehome, sign_in, register, forgot_password, reset_password, otp, error_page
from django.conf.urls.static import static

urlpatterns = [
    path('', sitehome, name = 'site_home'),
    path('login/', sign_in, name = 'site_login'),
    path('register/', register, name = 'site_register'),
    path('forgotpassword/', forgot_password, name = 'site_forgotpassword'),
    path('resetpassword/', reset_password, name = 'site_resetpassword'),
    path('otp/', otp, name = 'site_otp'),
         path('404/', error_page, name='site_errorpage')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
