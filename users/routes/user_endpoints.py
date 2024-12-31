from django.urls import path
from users.views.user_view import Register, Login, UserManagement


urlpatterns = [
    path('user/login/', Login.as_view(), name='user_login'),
    path('get/all/users/', UserManagement.as_view(), name='users'),
    path('user/register/', Register.as_view(), name='user_register'),
    path('user/<int:user_id>', UserManagement.as_view(),  name='user_manage'),
    # path('users/<int:user_id>/manage', UserManagement.as_view(), name='user-manage'),
]