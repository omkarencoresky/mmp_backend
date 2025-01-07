from django.urls import path
from driver.views.driver_view import DriverManagement


urlpatterns = [
    # path('user/login/', Login.as_view(), name='user_login'),
    # path('get/all/users/', UserManagement.as_view(), name='users'),
    path('<uuid:user_id>', DriverManagement.as_view(), name='driver_register'),
    # path('user/<uuid:user_id>', UserManagement.as_view(),  name='user_manage'),
]