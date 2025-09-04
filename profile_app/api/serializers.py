from rest_framework import serializers
from coder.models import Profile




class CustomerProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for customer profiles, including linked user fields.
    """
    user = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    email = serializers.EmailField(source='user.email')
    created_at = serializers.DateTimeField(source='user.date_joined', read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'uploaded_at', 'type', 'email', 'created_at']

    def get_user(self, obj):
        return obj.user.id

    def get_username(self, obj):
        return obj.user.username

    def get_type(self, obj):
        return obj.user.type

    def to_representation(self, instance):
        """
        Ensures 'file' is never null in the response.
        """
        data = super().to_representation(instance)
        if data.get('file') is None:
            data['file'] = ''
        return data

    def update(self, instance, validated_data):
        """
        Updates profile and user email.
        """
        user_data = validated_data.pop('user', {})
        email = user_data.get('email')
        if email:
            instance.user.email = email
            instance.user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance




class BusinessProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for customer profiles, including linked user fields.
    """
    user = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    email = serializers.EmailField(source='user.email')
    created_at = serializers.DateTimeField(source='user.date_joined', read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'location', 'tel', 'description', 'working_hours', 'type', 'email', 'created_at']

    def get_user(self, obj):
        return obj.user.id

    def get_username(self, obj):
        return obj.user.username

    def get_type(self, obj):
        return obj.user.type

    def to_representation(self, instance):
        """
        Ensures 'file' is never null in the response.
        """
        data = super().to_representation(instance)
        if data.get('file') is None:
            data['file'] = ''
        return data

    def update(self, instance, validated_data):
        """
        Updates profile and user email.
        """
        user_data = validated_data.pop('user', {})
        email = user_data.get('email')
        if email:
            instance.user.email = email
            instance.user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
        

    

class CustomerProfileListSerializer(serializers.ModelSerializer):
    """
    Compact serializer for listing customer profiles.
    """
    user = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'uploaded_at', 'type']

    def get_user(self, obj): return obj.user.id
    def get_username(self, obj): return obj.user.username
    def get_type(self, obj): return obj.user.type

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data.get('file') is None:
            data['file'] = ''
        return data

    




class BusinessProfileListSerializer(CustomerProfileListSerializer):
    """
    Compact serializer for listing business profiles with extended fields.
    """
    class Meta:
        model = Profile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'location', 'tel', 'description', 'working_hours', 'type']
