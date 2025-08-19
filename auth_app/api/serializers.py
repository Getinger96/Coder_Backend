from rest_framework import serializers
from auth_app.models import User
from coder.models import Profile



class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password','type']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        repeated_password = validated_data.pop('repeated_password')

        if password != repeated_password:
            raise serializers.ValidationError({'error': 'Passwords do not match'})

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        print("User saved. Now creating profile...")
        profile = Profile.objects.create(user=user)
        print("Profile created:", profile)

        return user



    
    