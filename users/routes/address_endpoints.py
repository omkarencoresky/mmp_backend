from django.urls import path
from users.views.address_view import Addresses


urlpatterns = [
    path('address/get/<int:user_id>', Addresses.as_view()),
    path('address/<int:address_id>', Addresses.as_view()),

]