from rest_framework import generics
from .models import User, DynamicData
from .serializer import UserSerializer, DynamicDataSerializer
from .authentication import IsAuthenticated, generate_token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import google.generativeai as genai

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

    def perform_create(self, serializer):
        DynamicData.objects.filter(user=self.request.user).delete()
        serializer.save(user=self.request.user)
    
class DynamicDataUpdateView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [IsAuthenticated]
    queryset = DynamicData.objects.all()
    serializer_class = DynamicDataSerializer
    lookup_field = 'id'
    
class AIHealthEvaluationView(APIView):
    authentication_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user  

        try:
            user_data = User.objects.get(id=user.id)
            dynamic_data = DynamicData.objects.filter(user=user).first() 

            if not dynamic_data:
                return Response({"error": "No dynamic data found for the user"}, status=400)

            prompt_text = f"""
            Generate a structured health report and recommendations based on the following details:

            1. **Personal Information:**
               - Name: {user_data.full_name}
               - Age: {user_data.dob}
               - Gender: {user_data.gender}
               - Height: {user_data.height}
               - Weight: {user_data.weight}
               - City: {user_data.city}

            2. **Lifestyle Factors:**
               - Smoking: {dynamic_data.smoking}
               - Drinking: {dynamic_data.drinking}
               - Sleeping Hours: {dynamic_data.sleeping_hours}
               - Exercise Hours: {dynamic_data.exercise_hours}

            3. **Medical History:**
               - {dynamic_data.medical_history}

            Generate a structured health report with:
            - Overall health analysis (word count: 50)
            - Major risk factors (word count: 20)
            - Personalized preventive recommendations (word count: 50)
            - Future health risk prediction (word count: 30)
            """

            payload = {
                "contents": [{
                    "parts": [{"text": prompt_text}]
                }]
            }

            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(prompt_text)

            return Response({"health_report": response.text}, status=200)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        except Exception as e:
            return Response({"error": str(e)}, status=500)