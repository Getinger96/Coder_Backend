from rest_framework import generics,viewsets,filters,status
from .serializers import CustomerProfileSerializer, BusinessProfileSerializer,CustomerProfileListSerializer,BusinessProfileListSerializer
from coder.models import Profile
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated



class ProfileDetailView(generics.GenericAPIView):
    """
    Retrieve or partially update a user profile.

    Permissions:
        Only authenticated users.

    Behavior:
        GET: Returns the profile data. Uses different serializers for business and customer users.
        PATCH: Allows the owner of the profile to partially update it.
    """
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.user.type == 'business':
            return BusinessProfileSerializer
        else:
            return CustomerProfileSerializer

    def get(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(profile)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        profile = self.get_object()
        if profile.user != request.user:
            return Response({'detail': 'You do not have permission to edit this profile.'}, status=403)
        
        serializer_class = self.get_serializer_class()
        input_serializer = serializer_class(profile, data=request.data, partial=True)
        if input_serializer.is_valid():
            input_serializer.save()
            response_serializer = serializer_class(profile)
            return Response(response_serializer.data)
        return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileCustomerView(generics.ListAPIView):
    """
    List all customer profiles.

    Permissions:
        Only authenticated users.
    """
    queryset = Profile.objects.filter(user__type='customer')
    serializer_class = CustomerProfileListSerializer
    permission_classes = [IsAuthenticated]


class ProfileBusinessView(generics.ListAPIView):
    """
    List all business profiles.

    Permissions:
        Only authenticated users.
    """
    queryset = Profile.objects.filter(user__type='business')
    serializer_class = BusinessProfileListSerializer
    permission_classes = [IsAuthenticated]
