from django.urls import path
from package_provider.views.daily_itinerary_view import DailyItineraryManagement


urlpatterns = [
    path('user/<uuid:user_id>/package/<uuid:package_id>', DailyItineraryManagement.as_view()),
    path('user/<uuid:user_id>/itinerary/<uuid:itinerary_id>', DailyItineraryManagement.as_view())

]   