from rest_framework import serializers
from coder.models import Profile,OfferDetail, Offer,Order,Review
from django.db.models import Min


class OfferDetailHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    """
    Hyperlinked serializer for OfferDetail — only includes id and a detail URL.
    """
    class Meta:
        model = OfferDetail
        fields = ['id', 'url']
        extra_kwargs = {
            'url': {'view_name': 'offerdetail_detail', 'lookup_field': 'pk'}
        }


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Full serializer for offer detail block (basic/premium/etc.).
    """
    class Meta:
        model = OfferDetail
        fields = [
            'id',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type'
        ]
        extra_kwargs = {
            'offer_type': {
                'required': True,      # Pflichtfeld
                'allow_blank': False,  # leere Strings nicht erlaubt
            }
        }

    def validate_offer_type(self, value):
        if not value:
            raise serializers.ValidationError("Offer type is required.")
        return value


class OfferSerializer(serializers.ModelSerializer):
    """
    Serializer for creating/updating offers with nested OfferDetails.
    """
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    def create(self, validated_data):
        request = self.context.get('request')
        profile = Profile.objects.get(user=request.user)
        details_data = validated_data.pop('details')

        offer = Offer.objects.create(profile=profile, **validated_data)

        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)

        return offer
    
    """
    Update an Offer instance and its related details.

    - Updates main fields of the Offer.
    - If `details` are provided:
        * Validates presence of `offer_type`.
        * Ensures each `offer_type` exists for the Offer.
        * Updates the matching detail with new values.

    Returns:
        Offer: the updated instance.
    """

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data is not None:
            
            existing_details = {d.offer_type: d for d in instance.details.all()}

            for detail_data in details_data:
                offer_type = detail_data.get('offer_type')
                if not offer_type:
                    raise serializers.ValidationError({
                        "details": "Each detail must include a valid 'offer_type'."
                    })

                if offer_type not in existing_details:
                    raise serializers.ValidationError({
                        "details": f"OfferDetail with offer_type '{offer_type}' does not exist for this offer."
                    })

             
                detail = existing_details[offer_type]
                for attr, value in detail_data.items():
                    setattr(detail, attr, value)
                detail.save()

        return instance
    

class OfferDetailListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing OfferDetails with a generated URL.
    """
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        return f"/offerdetails/{obj.id}/"
    


class OfferListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing offers with summary details and min values.
    """
    user = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    details = OfferDetailListSerializer(many=True)

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at', 'details',
            'min_price', 'min_delivery_time', 'user_details'
        ]

    def get_user(self, obj): return obj.profile.user.id

    def get_user_details(self, obj):
        user = obj.profile.user
        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username
        }

    def get_min_price(self, obj):
        return obj.details.all().aggregate(Min('price'))['price__min']

    def get_min_delivery_time(self, obj):
        return obj.details.all().aggregate(Min('delivery_time_in_days'))['delivery_time_in_days__min']



class OfferDetailViewSerializer(serializers.ModelSerializer):
    """
    Detailed view serializer for a single offer.
    """
    user = serializers.SerializerMethodField()
    details = OfferDetailHyperlinkedSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at', 'details',
            'min_price', 'min_delivery_time',
        ]

    def get_user(self, obj): return obj.profile.user.id

    def get_details(self, obj):
        request = self.context.get('request')
        return [
            {
                'id': detail.id,
                'url': request.build_absolute_uri(f'/api/offerdetails/{detail.id}/')
            }
            for detail in obj.details.all()
        ]

    def get_min_price(self, obj):
        return obj.details.all().aggregate(Min('price'))['price__min']

    def get_min_delivery_time(self, obj):
        return obj.details.all().aggregate(Min('delivery_time_in_days'))['delivery_time_in_days__min']



class OrderSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for retrieving orders with full offer detail info.
    """
    customer_user = serializers.PrimaryKeyRelatedField(read_only=True)
    business_user = serializers.PrimaryKeyRelatedField(read_only=True)

    title = serializers.CharField(source='offer_detail.title', read_only=True)
    revisions = serializers.IntegerField(source='offer_detail.revisions', read_only=True)
    delivery_time_in_days = serializers.IntegerField(source='offer_detail.delivery_time_in_days', read_only=True)
    price = serializers.DecimalField(source='offer_detail.price', max_digits=10, decimal_places=2, read_only=True)
    features = serializers.JSONField(source='offer_detail.features', read_only=True)
    offer_type = serializers.CharField(source='offer_detail.offer_type', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer_user', 'business_user',
            'title', 'revisions', 'delivery_time_in_days',
            'price', 'features', 'offer_type',
            'status', 'created_at', 'updated_at',
        ]


class OrderCreateserializer(serializers.ModelSerializer):
    """
    Serializer for creating a new Order.

    Fields:
        offer_detail_id: Primary key of the OfferDetail being ordered.

    Methods:
        create: Creates a new Order using the logged-in customer's profile, the business profile
                from the OfferDetail, and sets status to 'in_progress' by default.
    """
    offer_detail_id = serializers.PrimaryKeyRelatedField(source='offer_detail', queryset=OfferDetail.objects.all())
  
    class Meta:
        model = Order
        fields = ['offer_detail_id']
        read_only_fields = ['status', 'created_at', 'updated_at']

    def create(self, validated_data):
        request = self.context.get('request')
        customer_profile = Profile.objects.get(user=request.user)

        offer_detail = validated_data['offer_detail']
        business_profile = offer_detail.offer.profile

        # Set status to 'in_progress' by default
        order = Order.objects.create(
            offer_detail=offer_detail,
            customer_user=customer_profile,
            business_user=business_profile,
            status='in_progress'
        )

        return order
    

class OrderUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer to update the status of an Order.

    Fields:
        status: new status of the Order.
    """
    class Meta:
        model = Order
        fields = ['status']


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing and updating Reviews.

    Fields:
        business_user: Profile of the reviewed business (read-only).
        reviewer: Profile of the reviewer (read-only).
        rating: Rating value.
        description: Review description.
        created_at: Creation timestamp (read-only).
        updated_at: Update timestamp (read-only).

    Methods:
        update: Only 'rating' and 'description' can be updated.
    """
    business_user = serializers.PrimaryKeyRelatedField(read_only=True)
    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'business_user', 'reviewer', 'created_at', 'updated_at']

    def update(self, instance, validated_data):
        allowed_fields = {'rating', 'description'}
        for field in validated_data:
            if field not in allowed_fields:
                raise serializers.ValidationError(f"The field '{field}' cannot be modified.")

        instance.rating = validated_data.get('rating', instance.rating)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class ReviewCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new Review.

    Fields:
        business_user: Business profile being reviewed (queryset restricted to business-type users).
        rating: Rating value.
        description: Review description.

    Methods:
        validate: Checks if the user has already reviewed this business.
        create: Creates a new Review with the current user as the reviewer.
    """
    business_user = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.filter(user__type='business'))

    class Meta:
        model = Review
        fields = ['business_user', 'rating', 'description']

    def validate(self, data):
        request = self.context.get('request')
        reviewer_profile = Profile.objects.get(user=request.user)

        if Review.objects.filter(
            reviewer=reviewer_profile,
            business_user=data['business_user']
        ).exists():
            raise serializers.ValidationError("You have already reviewed this business.")

        return data

    def create(self, validated_data):
        request = self.context.get('request')
        reviewer_profile = Profile.objects.get(user=request.user)

        return Review.objects.create(
            business_user=validated_data['business_user'],
            reviewer=reviewer_profile,
            rating=validated_data['rating'],
            description=validated_data.get('description', '')
        )