from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from langchain.llms import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from myapp.models import User
from myapp.utils import generate_token
import os

# Initialize Gemini LLM
llm = GoogleGenerativeAI(model="gemini-2.0-flash", api_key=os.getenv("GEMINI_API_KEY"))

class LoginView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        password = request.data.get("password")
        
        user = User.objects.filter(phone_number=phone_number).first()
        
        if user and password == user.password:
            token = generate_token(user)
            return Response({"token": token}, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class AIHealthEvaluationView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user  

        try:
            user_data = User.objects.get(id=user.id)
            
            # Define Prompt Template
            prompt_template = PromptTemplate(
                input_variables=["name", "age", "gender", "height", "weight", "city", "smoking", "drinking", "sleeping_hours", "exercise_hours", "medical_history"],
                template="""
                Act as a doctor and generate a structured health report without including personal details like name and city. 
                Ensure the report is professional, user-friendly, and concise.
                
                1. **Personal Information:**
                   - Age: {age}
                   - Gender: {gender}
                   - Height: {height}
                   - Weight: {weight}
                
                2. **Lifestyle Factors:**
                   - Smoking: {smoking}
                   - Drinking: {drinking}
                   - Sleeping Hours: {sleeping_hours}
                   - Exercise Hours: {exercise_hours}
                
                3. **Medical History:**
                   - {medical_history}
                
                Generate a structured health report with:
                - Overall health analysis (word count: 50)
                - Major risk factors (word count: 20)
                - Personalized preventive recommendations (word count: 50)
                - Future health risk prediction (word count: 30)
                """
            )

            # Create LLM Chain
            chain = LLMChain(llm=llm, prompt=prompt_template)

            # Generate health report
            health_report = chain.run(
                name=user_data.full_name,
                age=user_data.dob,
                gender=user_data.gender,
                height=user_data.height,
                weight=user_data.weight,
                city=user_data.city,
                smoking=user_data.smoking,
                drinking=user_data.drinking,
                sleeping_hours=user_data.sleeping_hours,
                exercise_hours=user_data.exercise_hours,
                medical_history=user_data.medical_history,
            )
            
            return Response({"health_report": health_report}, status=200)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        except Exception as e:
            return Response({"error": str(e)}, status=500)