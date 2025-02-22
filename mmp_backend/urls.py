"""
URL configuration for mmp_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    # -------------------------------Admin-----------------------
    path('admin/', admin.site.urls),


    # -------------------------------Users----------------------------
    path('api/', include('users.routes.user_endpoints')),
    path('api/address/', include('users.routes.address_endpoints')),
    path('api/company/', include('users.routes.company_endpoints')),


    # -------------------------------Common app-----------------------------
    path('api/permission/', include('common_app.routes.permission_endpoints')),
    path('api/user/permission/', include('common_app.routes.user_permission_endpoints')),
    path('api/tour/package/bidding/', include('common_app.routes.bidding_proposal_endpoints')),
    


    # -------------------------------Driver------------------------------------
    path('api/driver/', include('driver.routes.driver_endpoints')),


    # -------------------------------Travel Agency----------------------------------
    path('api/travel/agency/', include('travel_agency.routes.travel_agency_endpoints')),
    path('api/transport/vehicle/', include('travel_agency.routes.transport_vehicle_endpoints')),


    # -------------------------------Package Provider------------------------------------
    path('api/tour/package/', include('package_provider.routes.tour_package_endpoints')),
    path('api/daily/itinerary/', include('package_provider.routes.daily_itinerary_endpoints')),
    path('api/package/provider/', include('package_provider.routes.package_provider_endpoints')),
    path('api/package/bid/', include('package_provider.routes.tour_package_bid_endpoints')),
]
