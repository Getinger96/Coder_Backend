from rest_framework import generics,viewsets,filters,status
from .serializers import OfferSerializer,OfferListSerializer,OfferDetailViewSerializer,OfferDetailSerializer,OrderSerializer,OrderCreateserializer,OrderUpdateSerializer,ReviewCreateSerializer,ReviewSerializer
from coder.models import Profile,Offer,OfferDetail,Order,Review
from coder.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Min, Avg
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied, ValidationError
from.permissions import IsBusinessUserOrReadOnly, IsOwnerOrReadOnly, IsCustomerForPost, IsReviewOwnerOrReadOnly, IsBusinessForPatchOrAdminForDelete


class LargeResultsSetPagination(PageNumberPagination):
    """
    Pagination class to control page size and maximum page size.
    """
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 10000


class OfferView(generics.ListCreateAPIView):
    """
    List all offers or create a new offer.

    Permissions:
        Business users can create offers; others can read.

    Filtering:
        Supports filtering by creator_id, min_price, max_delivery_time.
        Supports search by title and description.
        Supports ordering by updated_at and min_price.

    Pagination:
        Uses LargeResultsSetPagination.
    """
    queryset = Offer.objects.all()
    permission_classes = [IsBusinessUserOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['profile__user_id']
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']
    ordering = ['updated_at']
    pagination_class = LargeResultsSetPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferSerializer  # Serializer for creating an offer
        return OfferListSerializer  # Serializer for listing offers

    def get_queryset(self):
     queryset = super().get_queryset()

    # Filter by creator_id
     creator_id = self.request.query_params.get('creator_id')
     if creator_id:
        queryset = queryset.filter(profile__user__id=creator_id)

    # Filter by min_price
     min_price = self.request.query_params.get('min_price')
     if min_price:
        try:
            min_price = float(min_price)
        except ValueError:
            raise ValidationError({"min_price": "Must be a number."})
        queryset = queryset.annotate(min_price=Min('details__price')) \
                           .filter(min_price__gte=min_price)

    # Filter by max_delivery_time
     max_delivery_time = self.request.query_params.get('max_delivery_time')
     if max_delivery_time:
        try:
            max_delivery_time = int(max_delivery_time)
        except ValueError:
            raise ValidationError({"max_delivery_time": "Must be an integer."})
        queryset = queryset.annotate(min_delivery_time=Min('details__delivery_time_in_days')) \
                           .filter(min_delivery_time__lte=max_delivery_time)

     return queryset


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a single offer.

    Permissions:
        Authenticated users can view.
        Only owners can edit or delete.

    Behavior:
        GET: Uses OfferDetailViewSerializer.
        PATCH, DELETE: Uses OfferSerializer.
    """
    queryset = Offer.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OfferDetailViewSerializer
        return OfferSerializer


class OfferDetailRetrieveView(generics.RetrieveAPIView):
    """
    Retrieve details of a specific OfferDetail.

    Permissions:
        Only authenticated users.
    """
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'


class OrderView(generics.ListCreateAPIView):
    """
    List all orders or create a new order.

    Permissions:
        Only customers can create orders.
    """
    queryset = Order.objects.all()
    permission_classes = [IsCustomerForPost]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateserializer
        return OrderSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create the order
        order = serializer.save()

        # Return full order data in response
        response_serializer = OrderSerializer(order, context={'request': request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific order.

    Permissions:
        Only business users can patch.
        Only admins can delete.
    """
    queryset = Order.objects.all()
    serializer_class = OrderUpdateSerializer
    lookup_field = 'pk'
    permission_classes = [IsBusinessForPatchOrAdminForDelete]

    def get_object(self):
        # Objekt holen (404 wenn nicht gefunden)
        obj = get_object_or_404(Order, pk=self.kwargs.get(self.lookup_field))
        # Danach die Berechtigungen prüfen
        self.check_object_permissions(self.request, obj)
        return obj

    def patch(self, request, *args, **kwargs):
        order = self.get_object()

        # Validate and save input data
        serializer = self.get_serializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # updated_at is updated automatically

        # Return full order data with all fields
        full_serializer = OrderSerializer(order, context={'request': request})
        return Response(full_serializer.data)


class BusinessUserOrderCountView(APIView):
    """
    Return the count of 'in_progress' orders for a specific business user.

    Permissions:
        Only authenticated users.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        user = get_object_or_404(User, id=business_user_id, type='business')

        count = Order.objects.filter(
            business_user__user=user,
            status='in_progress'
        ).count()

        return Response({'order_count': count}, status=status.HTTP_200_OK)


class BusinessUserOrderCompletedCountView(APIView):
    """
    Return the count of 'completed' orders for a specific business user.

    Permissions:
        Only authenticated users.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        user = get_object_or_404(User, id=business_user_id, type='business')

        count = Order.objects.filter(
            business_user__user=user,
            status='completed'
        ).count()

        return Response({'completed_order_count': count}, status=status.HTTP_200_OK)


class ReviewCreateView(generics.ListCreateAPIView):
    """
    List all reviews or create a new review.

    Permissions:
        Only customers can create reviews.

    Ordering:
        Can order by 'updated_at' or 'rating'.

    Filtering:
        Can filter by business_user_id and reviewer_id.
    """
    queryset = Review.objects.all()
    permission_classes = [IsCustomerForPost]
    ordering_fields = ['updated_at', 'rating']
    ordering = ['updated_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewCreateSerializer
        return ReviewSerializer
    
    def get_queryset(self):
        queryset = Review.objects.all()

        business_user_id = self.request.query_params.get('business_user_id')
        if business_user_id:
            queryset = queryset.filter(business_user__user__id=business_user_id)

        reviewer_id = self.request.query_params.get('reviewer_id')
        if reviewer_id:
            queryset = queryset.filter(reviewer__user__id=reviewer_id)

        ordering = self.request.query_params.get('ordering')
        if ordering in ['updated_at', 'rating']:
            queryset = queryset.order_by(ordering)

        return queryset

    def create(self, request, *args, **kwargs):
        # Validation handled by permission
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = serializer.save()

        output_serializer = ReviewSerializer(review)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a review.

    Permissions:
        Only the reviewer may update or delete their review.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsReviewOwnerOrReadOnly]

    def get_object(self):
        review = super().get_object()
        # Permission check: only reviewer may modify
        if review.reviewer.user != self.request.user:
            raise PermissionDenied("You are not allowed to edit or delete this review.")
        return review


class BaseInfoView(APIView):
    """
    Provides aggregated base information about the system.

    GET:
        Returns:
            - Total number of reviews
            - Average rating across all reviews
            - Total number of business profiles
            - Total number of offers

    Error Handling:
        Returns 500 with a generic error message if an exception occurs.
    """

    permission_classes = [AllowAny]
    def get(self, request):
        try:
            review_count = Review.objects.count()
            average_rating = Review.objects.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0.0
            business_profile_count = Profile.objects.filter(user__type='business').count()
            offer_count = Offer.objects.count()

            data = {
                "review_count": review_count,
                "average_rating": round(average_rating, 1),
                "business_profile_count": business_profile_count,
                "offer_count": offer_count
            }
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"detail": "An internal error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
