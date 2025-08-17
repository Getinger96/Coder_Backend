from rest_framework import serializers
from models import User



class RegistrationSerializer(serializers.Serializer):
    

     class Meta:
        model = User
        fields = ['fullname', 'email', 'password', 'repeated_password']
        