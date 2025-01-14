from django.urls import path
from users.views.user_view import Register, Login, UserManagement


urlpatterns = [


    #----Registration-----
    path('user/register/', Register.as_view(), name='user_register'),
    

    #----Login-----
    path('user/login/', Login.as_view(), name='user_login'),
    path('user/validate/otp/<uuid:user_id>', Login.as_view(), name='user_login'),


    #----Manage Users-----
    path('users/', UserManagement.as_view(), name='users'),
    path('user/<uuid:user_id>', UserManagement.as_view(),  name='user_manage'),
]