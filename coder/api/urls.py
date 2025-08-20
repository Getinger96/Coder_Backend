from django.urls import path
from .views import ProfileDetailView,ProfileCustomerView, ProfileBusinessView, OfferViewSet




urlpatterns = [
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/customer/', ProfileCustomerView.as_view(), name='profile_customer'),
    path('profile/business/', ProfileBusinessView.as_view(), name='profile_business'),
    path('offers/', OfferViewSet.as_view({'get': 'list', 'post': 'create'}), name='offer_list'),
    

]
   