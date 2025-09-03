from .serializers import  RegistrationSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status



class RegistrationView(APIView):
    """
    API endpoint for user registration.
    Allows any user (authenticated or not) to create a new account.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle POST requests to register a new user.

        - Validates input using RegistrationSerializer
        - Creates a new user and their profile
        - Returns an auth token along with user info
        """
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)

            data = {
                'token': token.key,
                'username': saved_account.username,
                'email': saved_account.email,
                'user_id': saved_account.id
            }

            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=400)


class CustomLoginView(ObtainAuthToken):
    """
    Custom login endpoint using token authentication.
    Returns user info along with the token.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle POST requests for login.

        - Validates credentials using DRF's built-in serializer
        - Returns a token and user details if valid
        """
        serializer = self.serializer_class(data=request.data)
        data = {}

        if serializer.is_valid():
         user = serializer.validated_data['user']
         token, created = Token.objects.get_or_create(user=user)
         return Response({
         'token': token.key,
         'username': user.username,
         'email': user.email,
         'user_id': user.id
    }, status=status.HTTP_200_OK)
        else:
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




    
    