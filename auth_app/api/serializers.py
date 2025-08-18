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
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        
        Profile.objects.create(user=user)

        return user

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
    


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['file', 'location', 'tel', 'description', 'working_hours']
    
    