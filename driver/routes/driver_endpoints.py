from django.urls import path
from driver.views.driver_view import DriverManagement


urlpatterns = [
    path('user/<uuid:user_id>', DriverManagement.as_view(), name='driver_register'),
    path('user/<uuid:user_id>/driver/<uuid:driver_id>', DriverManagement.as_view(), name='driver_register'),
]