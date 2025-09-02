from rest_framework import serializers
from auth_app.models import User
from coder.models import Profile



class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.
    Includes password confirmation and creates a Profile.
    """

    repeated_password = serializers.CharField(write_only=True)
    """Field to confirm the password (not saved in the database)."""

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        """Hide the password from API responses."""

    def create(self, validated_data):
        """
        Create a new user after checking password match,
        and automatically create a related Profile.
        """
        password = validated_data.pop('password')
        repeated_password = validated_data.pop('repeated_password')

        if password != repeated_password:
            raise serializers.ValidationError({'error': 'Passwords do not match'})

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        Profile.objects.create(user=user)

        return user



    
    