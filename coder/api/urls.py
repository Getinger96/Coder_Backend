from django.urls import path
from .views import  OfferView,OfferDetailView,OfferDetailRetrieveView,OrderView,OrderDetailView,BusinessUserOrderCountView,BusinessUserOrderCompletedCountView,ReviewCreateView,ReviewDetailView,BaseInfoView


urlpatterns = [
   
    path('offers/', OfferView.as_view(), name='offer_list'),
    path('offers/<int:pk>/', OfferDetailView.as_view(), name='offer_detail'),
    path('offerdetails/<int:pk>/', OfferDetailRetrieveView.as_view(), name='offerdetail_detail'),
    path('orders/', OrderView.as_view(), name='order_list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('order-count/<int:business_user_id>/', BusinessUserOrderCountView.as_view(), name='order-count'),
    path('completed-order-count/<int:business_user_id>/', BusinessUserOrderCompletedCountView.as_view(), name='order-completed-count'),
    path('reviews/', ReviewCreateView.as_view(), name='review-create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('base-info/', BaseInfoView.as_view(), name='base-info'),



]
   