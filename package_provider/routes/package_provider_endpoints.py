from django.urls import path
from package_provider.views.package_provider_view import PackageProvider


urlpatterns = [
    path('create/<uuid:creator_id>', PackageProvider.as_view()),
]