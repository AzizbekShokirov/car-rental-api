from django.urls import path
from .views import (
    CarListCreateView,
    CarDetailView, 
    CarByVinView,
    RentalListCreateView,
    RentalDetailView,
    RentalOverdueView,
    RentPriceListView
)

urlpatterns = [
    # Car endpoints
    path('cars/', CarListCreateView.as_view(), name='car-list-create'),
    path('cars/<int:pk>/', CarDetailView.as_view(), name='car-detail'),
    path('cars/vin/', CarByVinView.as_view(), name='car-by-vin'),
    
    # Rental endpoints
    path('rentals/', RentalListCreateView.as_view(), name='rental-list-create'),
    path('rentals/<int:pk>/', RentalDetailView.as_view(), name='rental-detail'),
    path('rentals/overdue/', RentalOverdueView.as_view(), name='rental-overdue'),
    
    # RentPrice endpoints
    path('rentprices/', RentPriceListView.as_view(), name='rentprice-list'),
]