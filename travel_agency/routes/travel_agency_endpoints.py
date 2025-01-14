from django.urls import path
from travel_agency.views.travel_agency_view import TravelAgency


urlpatterns = [
    path('create/<uuid:user_id>', TravelAgency.as_view()),
]