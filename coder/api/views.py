from rest_framework import generics,viewsets,filters,status
from .serializers import CustomerProfileSerializer, BusinessProfileSerializer,CustomerProfileListSerializer,BusinessProfileListSerializer,OfferSerializer,OfferListSerializer,OfferDetailViewSerializer,OfferDetailHyperlinkedSerializer,OrderSerializer,OrderCreateserializer,OrderUpdateSerializer,ReviewCreateSerializer,ReviewSerializer
from coder.models import Profile,Offer,OfferDetail,Order,Review
from coder.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Min
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied



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



class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()

    def get_serializer_class(self):
       if self.request.method == 'POST':
           return OrderCreateserializer
       return OrderSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Bestellung erstellen
        order = serializer.save()

        # Für die Response den vollständigen Serializer verwenden
        response_serializer = OrderSerializer(order, context={'request': request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderUpdateSerializer
    lookup_field = 'pk'    

    def patch(self, request, *args, **kwargs):
        order = self.get_object()

        # Eingabedaten validieren und speichern
        serializer = self.get_serializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Hier wird `updated_at` automatisch aktualisiert

        # Jetzt den vollständigen Output mit allen Feldern zurückgeben
        full_serializer = OrderSerializer(order, context={'request': request})
        return Response(full_serializer.data)




class BusinessUserOrderCountView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
     print("business_user_id:", business_user_id)
    
     try:
        user = User.objects.get(id=business_user_id)
        print("User gefunden:", user)
        print("User-Typ:", user.type)
     except User.DoesNotExist:
        print("User nicht gefunden")

     user = get_object_or_404(User, id=business_user_id, type='business')

     count = Order.objects.filter(
        business_user__user=user,
        status='in_progress'
     ).count()

     return Response({'order_count': count}, status=status.HTTP_200_OK)
    



class BusinessUserOrderCompletedCountView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
    
    
   
     user = User.objects.get(id=business_user_id)
      
    

     user = get_object_or_404(User, id=business_user_id, type='business')

     count = Order.objects.filter(
        business_user__user=user,
        status='completed'
     ).count()

     return Response({'completed_order_count': count}, status=status.HTTP_200_OK)
    


class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    # permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewCreateSerializer
        return ReviewSerializer

    def create(self, request, *args, **kwargs):
        # Stelle sicher, dass nur Kunden Bewertungen schreiben dürfen
        if request.user.type != 'customer':
            return Response({'detail': 'Nur Kunden dürfen Bewertungen erstellen.'},
                            status=status.HTTP_403_FORBIDDEN)

        # ReviewCreateSerializer validiert die Eingabe
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = serializer.save()

        # Gebe die komplette Bewertung mit dem ReviewSerializer zurück
        output_serializer = ReviewSerializer(review)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
    


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        review = super().get_object()
        # Berechtigungsprüfung: Nur Ersteller darf ändern/löschen
        if review.reviewer.user != self.request.user:
            raise PermissionDenied("Du bist nicht berechtigt, diese Bewertung zu bearbeiten oder zu löschen.")
        return review