from rest_framework import serializers
from auth_app.models import User



class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password','type']
        extra_kwargs = {
            'password': {'write_only': True},
         }
      
    def save(self):
        pw=self.validated_data['password']
        repeated_pw=self.validated_data['repeated_password']
        if pw != repeated_pw:
            raise serializers.ValidationError({'error':'passwords do not match'})
        
        account= User(email=self.validated_data['email'],
                      username=self.validated_data['username'],
                      type=self.validated_data['type'])
        account.set_password(pw)
        account.save()
        return account