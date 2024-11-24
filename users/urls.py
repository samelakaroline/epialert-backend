from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserRegistrationView, CustomAuthToken, UserDetailView

urlpatterns = [
    path('login/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('profile/', UserDetailView.as_view(), name='user-profile'),
    ]
