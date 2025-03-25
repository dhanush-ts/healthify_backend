from rest_framework import generics
from .models import User, DynamicData
from .serializer import UserSerializer, DynamicDataSerializer
from .authentication import IsAuthenticated, generate_token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserUpdateView(generics.RetrieveUpdateAPIView):
    authentication_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
class LoginView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        
        user = User.objects.filter(phone_number=phone_number).first()
        
        if user and password==user.password:
            token = generate_token(user)
            return Response({'token': token}, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
class DynamicDataView(generics.CreateAPIView):
    authentication_classes = [IsAuthenticated]
    queryset = DynamicData.objects.all()
    serializer_class = DynamicDataSerializer
    
class DynamicDataUpdateView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [IsAuthenticated]
    queryset = DynamicData.objects.all()
    serializer_class = DynamicDataSerializer
    lookup_field = 'id'
    
