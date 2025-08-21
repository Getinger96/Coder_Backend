from django.urls import path
from .views import ProfileDetailView,ProfileCustomerView, ProfileBusinessView, OfferView,OfferDetailView




urlpatterns = [
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/customer/', ProfileCustomerView.as_view(), name='profile_customer'),
    path('profile/business/', ProfileBusinessView.as_view(), name='profile_business'),
    path('offers/', OfferView.as_view(), name='offer_list'),
    path('offers/<int:pk>/', OfferDetailView.as_view(), name='offer_detail'),


]
   