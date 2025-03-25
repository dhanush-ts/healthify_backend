from django.urls import path
from .views import UserCreateView, UserUpdateView, LoginView, DynamicDataUpdateView, DynamicDataView

urlpatterns = [
    path('signup/', UserCreateView.as_view(), name='user-create'),
    path('update-static/<int:id>/', UserUpdateView.as_view(), name='user-update'),
    path('login/', LoginView.as_view(), name='login'),
    path('dynamic-create/', DynamicDataView.as_view(), name='dynamic-create'),
    path('dynamic/<int:id>/', DynamicDataUpdateView.as_view(), name='update-dynamic'),
]