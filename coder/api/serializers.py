from rest_framework import serializers
from coder.models import Profile,OfferDetail, Offer,Order,Review
from django.db.models import Min




class OfferDetailHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'url']
        extra_kwargs = {
            'url': {'view_name': 'offerdetail_detail', 'lookup_field': 'pk'}
        }




class CustomerProfileSerializer(serializers.ModelSerializer):
    user=serializers.SerializerMethodField('get_user')
    username = serializers.SerializerMethodField('get_username')
    type = serializers.SerializerMethodField()
    email = serializers.EmailField(source='user.email')
    created_at = serializers.DateTimeField(source='user.date_joined', read_only=True)
    

    
    class Meta:
        model = Profile
        fields = ['user', 'username', 'first_name', 'last_name','file', 'uploaded_at','type','email','created_at']

    def get_user(self, obj):
        return obj.user.id
            
       
    def get_username(self, obj):
     return obj.user.username
    
    def get_type(self, obj):
        return obj.user.type

    def to_representation(self, instance):
     data = super().to_representation(instance)
     if data.get('file') is None:
        data['file'] = ''
     return data

    

    def update(self, instance, validated_data):
        # user-Daten extrahieren
        user_data = validated_data.pop('user', {})

        # email updaten, falls dabei
        email = user_data.get('email')
        if email:
            instance.user.email = email
            instance.user.save()

        # Profilfelder updaten
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance




class BusinessProfileSerializer(serializers.ModelSerializer):
    user=serializers.SerializerMethodField('get_user')
    username = serializers.SerializerMethodField('get_username')
    type = serializers.SerializerMethodField()
    email = serializers.EmailField(source='user.email')
    created_at = serializers.DateTimeField(source='user.date_joined', read_only=True)
    

    
    class Meta:
        model = Profile
        fields = ['user', 'username', 'first_name', 'last_name','file','location','tel','description','working_hours','type','email','created_at']

    def get_user(self, obj):
        return obj.user.id
    
    def get_username(self, obj):
     return obj.user.username
    
    def get_type(self, obj):
        return obj.user.type

    def to_representation(self, instance):
     data = super().to_representation(instance)
     if data.get('file') is None:
        data['file'] = ''
     return data

    

    def update(self, instance, validated_data):
        # user-Daten extrahieren
        user_data = validated_data.pop('user', {})

        # email updaten, falls dabei
        email = user_data.get('email')
        if email:
            instance.user.email = email
            instance.user.save()

        # Profilfelder updaten
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
        

    

class CustomerProfileListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    

    class Meta:
        model = Profile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'uploaded_at', 'type']

    def get_user(self, obj):
        return obj.user.id

    def get_username(self, obj):
        return obj.user.username

    def get_type(self, obj):
        return obj.user.type

    def to_representation(self, instance):
     data = super().to_representation(instance)
     if data.get('file') is None:
        data['file'] = ''
     return data

    




class BusinessProfileListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    

    class Meta:
        model = Profile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'location', 'tel', 'description', 'working_hours', 'type']

    def get_user(self, obj):
        return obj.user.id

    def get_username(self, obj):
        return obj.user.username

    def get_type(self, obj):
        return obj.user.type

    def to_representation(self, instance):
     data = super().to_representation(instance)
     if data.get('file') is None:
        data['file'] = ''
     return data

    


class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']




class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    def create(self, validated_data):
     request = self.context.get('request')
     user = request.user
     profile = Profile.objects.get(user=user)  # falls du ein separates Profile-Modell nutzt

     details_data = validated_data.pop('details')
     offer = Offer.objects.create(profile=profile, **validated_data)

     for detail_data in details_data:
        OfferDetail.objects.create(offer=offer, **detail_data)

     return offer
    

    def update(self, instance, validated_data):
     details_data = validated_data.pop('details', None)

    # Update einfache Felder
     for attr, value in validated_data.items():
        setattr(instance, attr, value)
     instance.save()

     if details_data is not None:
        # Alle bestehenden OfferDetails holen
        existing_details = {d.offer_type: d for d in instance.details.all()}

        for detail_data in details_data:
            offer_type = detail_data.get('offer_type')

            if offer_type in existing_details:
                # Detail aktualisieren
                detail = existing_details[offer_type]
                for attr, value in detail_data.items():
                    setattr(detail, attr, value)
                detail.save()
            else:
                # Neues Detail anlegen
                OfferDetail.objects.create(offer=instance, **detail_data)

     return instance
    

class OfferDetailListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        return f"/offerdetails/{obj.id}/"
    


class OfferListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    details = OfferDetailListSerializer(many=True)
    
    class Meta:
        model = Offer
        fields = [
            'id',
            'user',
            'title',
            'image',
            'description',
            'created_at',
            'updated_at',
            'details',
            'min_price',
            'min_delivery_time',
            'user_details'
        ]

    def get_user(self, obj):
        return obj.profile.user.id

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
    user = serializers.SerializerMethodField()
    details = OfferDetailHyperlinkedSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id',
            'user',
            'title',
            'image',
            'description',
            'created_at',
            'updated_at',
            'details',
            'min_price',
            'min_delivery_time',
        ]

    def get_user(self, obj):
        return obj.profile.user.id

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
            'id',
            'customer_user',
            'business_user',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
            'status',
            'created_at',
            'updated_at',
        ]

class OrderCreateserializer(serializers.ModelSerializer):
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
        # Setze den Status standardmäßig auf 'in_progress'
       order = Order.objects.create(
            offer_detail=offer_detail,
            customer_user=customer_profile,
            business_user=business_profile,
            status='in_progress'
        )

       return order
    

class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']




class ReviewSerializer(serializers.ModelSerializer):
    business_user = serializers.PrimaryKeyRelatedField(read_only=True)
    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'business_user', 'reviewer', 'created_at', 'updated_at']

    def update(self, instance, validated_data):
        # Nur rating und description dürfen geändert werden
        allowed_fields = {'rating', 'description'}
        for field in validated_data:
            if field not in allowed_fields:
                raise serializers.ValidationError(f"Das Feld '{field}' darf nicht bearbeitet werden.")

        # Werte aktualisieren
        instance.rating = validated_data.get('rating', instance.rating)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

    

class ReviewCreateSerializer(serializers.ModelSerializer):
    business_user = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.filter(user__type='business'))
   

    class Meta:
        model = Review
        fields = ['business_user', 'rating', 'description']

    def validate(self, data):
        request = self.context.get('request')
        reviewer_profile = Profile.objects.get(user=request.user)

        # Prüfung: hat der Benutzer bereits eine Bewertung für diesen Business?
        if Review.objects.filter(
            reviewer=reviewer_profile,
            business_user=data['business_user']
        ).exists():
            raise serializers.ValidationError("Du hast diesen Anbieter bereits bewertet.")

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