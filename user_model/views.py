from rest_framework import generics
from .models import User
from .serializer import UserSerializer
from .authentication import IsAuthenticated, generate_token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import google.generativeai as genai
from django.conf import settings

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserUpdateView(generics.RetrieveUpdateAPIView):
    authentication_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user

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

class AIHealthEvaluationView(APIView):
    authentication_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user  
        try:
            user_data = User.objects.get(id=user.id)
            prompt_text = f"""
            Act as a doctor and give as if you are generating a medical report for the person and again dont add unwanted 
            the personal information in the response like name city etc and in the response dont give as md it should be humanized and 
            and it should be professionally user friendly 
            
            just give the output directly don't say like : Okay, let's put together a health report based on the information provided. Here's what I've got it shouldnt be like a api request
            instead start from : you appear ...
            Generate a structured health report and recommendations based on the following details:

            1. **Personal Information:**
               - Name: {user_data.full_name}
               - Age: {user_data.dob}
               - Gender: {user_data.gender}
               - Height: {user_data.height}
               - Weight: {user_data.weight}
               - City: {user_data.city}
               
               dont repeat this personal information in the response anywhere and dont give a response like ai just give like a doctor

            2. **Lifestyle Factors:**
               - Smoking: {user_data.smoking}
               - Drinking: {user_data.drinking}
               - Sleeping Hours: {user_data.sleeping_hours}
               - Exercise Hours: {user_data.exercise_hours}

            3. **Medical History:**
               - {user_data.medical_history}

            Generate a structured health report with:
            - Overall health analysis (word count: 50)
            - Major risk factors (word count: 20)
            - Personalized preventive recommendations (word count: 50)
            - Future health risk prediction (word count: 30)
            
            if they have any bad habits tell few advices to follow to stop them in a favaroble way
            """

            payload = {
                "contents": [{
                    "parts": [{"text": prompt_text}]
                }]
            }

            model = genai.GenerativeModel(settings.GEN_AI_KEY)
            response = model.generate_content(prompt_text)

            return Response({"health_report": response.text}, status=200)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)