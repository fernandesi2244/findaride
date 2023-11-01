from rest_framework import generics, status, views, viewsets
from rest_framework import permissions
from .serializers import LoginSerializer, SignUpSerializer, UserSerializer
from django.contrib.auth import login
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from secrets import token_urlsafe

from django.core.mail import send_mail
from django.conf import settings

from django.utils import timezone

from .models import ActivationToken

UserModel = get_user_model()

class LoginView(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)
    

class IsLoggedInView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        if request.user.is_authenticated:
            return Response({'isAuthenticated': True}, status=status.HTTP_200_OK)
        else:
            return Response({'isAuthenticated': False}, status=status.HTTP_200_OK)
        
class CurrentUserView(views.APIView):
    def get(self, request):
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
        

class ActivateUserView(views.APIView):
    def post(self, request, *args, **kwargs):
        token_string=self.kwargs.get("token")

        try:
            token = ActivationToken.objects.get(token=token_string)

            if token.expiry >= timezone.now():
                user = token.user
                user.email_verified = True
                user.save()
                return Response(status=status.HTTP_202_ACCEPTED)
            else:
                return Response(status=status.HTTP_410_GONE)

        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class SignUpView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token_instance = ActivationToken.objects.create(
            token = token_urlsafe(32),
            user = user
        )

        # ACCOUNT ACTIVATION EMAIL (SET UP LATER)
        #subject = "Test"
        #message = f"http://127.0.0.1:8000/activate/{token_instance.token}/"
        #email_from = settings.EMAIL_HOST_USER
        #recipient_list = [user.email,]
        #send_mail( subject, message, email_from, recipient_list )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    