from django.urls import path
from users.views.user_view import Register, Login, UserManagement


urlpatterns = [
    path('users/', UserManagement.as_view(), name='users'),
    path('user/login/', Login.as_view(), name='user_login'),
    path('user/register/', Register.as_view(), name='user_register'),
    path('user/<uuid:user_id>', UserManagement.as_view(),  name='user_manage'),
]