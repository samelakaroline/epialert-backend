from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer, UserSerializer

User = get_user_model()

# View para cadastro de usuário via API
@permission_classes([AllowAny])
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View para login baseado em HTML
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirecione para o dashboard ou outra página após login bem-sucedido
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

# View para login com autenticação de token via API
@permission_classes([AllowAny])
class CustomAuthToken(APIView):
    def post(self, request, *args, **kwargs):
        username_or_email = request.data.get('username_or_email')
        password = request.data.get('password')
        
        # Verifica se os campos foram preenchidos
        if not username_or_email or not password:
            return Response({'error': 'Both username/email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verifica se o valor inserido é um email ou username
            user = User.objects.filter(email=username_or_email).first() if '@' in username_or_email else User.objects.filter(username=username_or_email).first()
            
            if user and user.check_password(password):
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# View para detalhes do usuário logado (retorna os dados do próprio usuário autenticado)
@permission_classes([IsAuthenticated])
class UserDetailView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user  # Obtém o usuário autenticado
        serializer = UserSerializer(user)  # Serializa os dados do usuário
        return Response(serializer.data, status=status.HTTP_200_OK)
