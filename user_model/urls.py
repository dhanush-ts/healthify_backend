from django.urls import path
from .views import UserCreateView, UserUpdateView, LoginView, AIHealthEvaluationView, AIHealthChatView

urlpatterns = [
    path('signup/', UserCreateView.as_view(), name='user-create'),
    path('update-static/', UserUpdateView.as_view(), name='user-update'),
    path('login/', LoginView.as_view(), name='login'),
    path('health-evaluation/', AIHealthEvaluationView.as_view(), name='ai-health-evaluation'),
    path('health-chat/', AIHealthChatView.as_view(), name='ai-health-chat'),
]