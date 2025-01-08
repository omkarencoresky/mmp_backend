from django.urls import path
from travel_agency.views.travel_agency_view import TravelAgency


urlpatterns = [
    path('transport/vehicle/<uuid:user_id>', TravelAgency.as_view()),
    path('transport/vehicle/get/<uuid:user_id>', TravelAgency.as_view()),
    path('transport/vehicle/<uuid:transport_vehicle_id>', TravelAgency.as_view()),
]