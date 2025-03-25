from django.urls import path
from .views import UserCreateView, UserUpdateView, LoginView

urlpatterns = [
    path('create/', UserCreateView.as_view(), name='user-create'),
    path('update/<int:id>/', UserUpdateView.as_view(), name='user-update'),
    path('login/', LoginView.as_view(), name='login'),
]
