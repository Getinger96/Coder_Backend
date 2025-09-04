from django.urls import path
from .views import ProfileDetailView,ProfileCustomerView, ProfileBusinessView




urlpatterns = [
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profiles/customer/', ProfileCustomerView.as_view(), name='profile_customer'),
    path('profiles/business/', ProfileBusinessView.as_view(), name='profile_business'),
    



]
   