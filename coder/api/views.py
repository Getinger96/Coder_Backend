from rest_framework import generics,viewsets
from .serializers import CustomerProfileSerializer, BusinessProfileSerializer,CustomerProfileListSerializer,BusinessProfileListSerializer,OfferSerializer
from coder.models import Profile,Offer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated







class ProfileDetailView(generics.GenericAPIView):
    queryset = Profile.objects.all()
    permission_classes= [IsAuthenticated]
    
    
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
    queryset = Profile.objects.filter(user__type='customer')
    serializer_class = CustomerProfileListSerializer
    permission_classes = [IsAuthenticated]

    
    

class ProfileBusinessView(generics.ListAPIView):
    queryset = Profile.objects.filter(user__type='business')
    serializer_class = BusinessProfileListSerializer
    permission_classes = [IsAuthenticated]

    

class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer