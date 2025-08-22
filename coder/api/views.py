from rest_framework import generics,viewsets,filters
from .serializers import CustomerProfileSerializer, BusinessProfileSerializer,CustomerProfileListSerializer,BusinessProfileListSerializer,OfferSerializer,OfferListSerializer,OfferDetailViewSerializer,OfferDetailHyperlinkedSerializer
from coder.models import Profile,Offer,OfferDetail
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Min
from rest_framework.pagination import PageNumberPagination



class LargeResultsSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 10000





class ProfileDetailView(generics.GenericAPIView):
    queryset = Profile.objects.all()
    permission_classes= [IsAuthenticated]
    
    
    def get_serializer_class(self):
          if self.request.user.type == 'business':
                return BusinessProfileSerializer
          else:
                return CustomerProfileSerializer

   
    def get(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(profile)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        profile = self.get_object()
        if profile.user != request.user:
         return Response({'detail': 'You do not have permission to edit this profile.'}, status=403)
        
        serializer_class = self.get_serializer_class()
        input_serializer = serializer_class(profile, data=request.data, partial=True)
        if input_serializer.is_valid():
            input_serializer.save()
            response_serializer = serializer_class(profile)
            return Response(response_serializer.data)
        return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ProfileCustomerView(generics.ListAPIView):
    queryset = Profile.objects.filter(user__type='customer')
    serializer_class = CustomerProfileListSerializer
    permission_classes = [IsAuthenticated]

    
    

class ProfileBusinessView(generics.ListAPIView):
    queryset = Profile.objects.filter(user__type='business')
    serializer_class = BusinessProfileListSerializer
    permission_classes = [IsAuthenticated]

    

class OfferView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['profile__user_id']
    search_fields=['title', 'description']
    ordering_fields = [ 'updated_at','min_price']
    ordering=['updated_at']
    pagination_class = LargeResultsSetPagination
    

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferSerializer  # Für Erstellung
        return OfferListSerializer  # Für GET-Listenansicht

    def get_queryset(self):
        queryset = Offer.objects.all()

        # Filter: creator_id
        creator_id = self.request.query_params.get('creator_id')
        if creator_id is not None:
            queryset = queryset.filter(profile__user__id=creator_id)

        # Annotation für min_price
        min_price = self.request.query_params.get('min_price')
        if min_price is not None:
            queryset = queryset.annotate(min_price=Min('details__price'))\
                               .filter(min_price__gte=min_price)

        # Annotation für max_delivery_time
        max_delivery_time = self.request.query_params.get('max_delivery_time')
        if max_delivery_time is not None:
            queryset = queryset.annotate(min_delivery_time=Min('details__delivery_time_in_days'))\
                               .filter(min_delivery_time__lte=max_delivery_time)

        return queryset
    




class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
     queryset = Offer.objects.all()
     
     lookup_field = 'pk'

     def get_serializer_class(self):
        if self.request.method == 'GET':
            return OfferDetailViewSerializer  # Für GET-Anfragen (z. B. mit Hyperlinks, min_price etc.)
        return OfferSerializer  # Für PATCH und DELETE



class OfferDetailRetrieveView(generics.RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailHyperlinkedSerializer