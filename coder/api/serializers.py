from rest_framework import serializers
from coder.models import Profile,OfferDetail, Offer









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