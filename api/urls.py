from django.contrib import admin
from django.urls import path,include
from api.views import UserRegistationView,LoginView,UserProfileView,UserResetPassword,SendpasswordEmail,PasswordResertView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',UserRegistationView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('profile/',UserProfileView.as_view(),name='profile'),
    path('changepassword/',UserResetPassword.as_view(),name='changepassword'),
    path('resertpassword/',SendpasswordEmail.as_view(),name='resertpassword'),
    path('resetpassword/<udi>/<token>',PasswordResertView.as_view(),name='resetpassword'),
    
    
    
]
