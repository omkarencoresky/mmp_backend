from django.urls import path
from driver.views.driver_view import DriverManagement


urlpatterns = [
    path('', DriverManagement.as_view()),
    path('<uuid:driver_id>', DriverManagement.as_view(), name='driver_register'),
    path('user/<uuid:user_id>', DriverManagement.as_view(), name='driver_register'),
]