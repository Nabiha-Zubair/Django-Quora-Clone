# views.py

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
import threading

from .serializer import UserModelSerializer
from .helpers import generate_token, get_tokens_for_user
from .permissions import CheckAuthenticatedUser
from .models import User
from .auth.custom_auth import CustomAuthentication
class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()
        print('email sent:')


def send_activation_email(user, requestuest):
    current_site = get_current_site(requestuest)
    email_subject = 'Activate your account'
    email_body = render_to_string('email/activate-email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })
    try:
        email = EmailMessage(subject=email_subject, body=email_body,
                             from_email=settings.EMAIL_FROM_USER,
                             to=[user.email]
                             )
        if not settings.TESTING:
            EmailThread(email).start()
    except Exception as e:
        raise e


@csrf_exempt
@api_view(['POST'])
def signupView(request):
    if request.method == 'POST':
        try:
            serializer = UserModelSerializer(data=request.data)

            if serializer.is_valid():
                user = serializer.save()
                send_activation_email(user, request)
                return Response({'message': 'Signup successful', 'user': serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_requestUEST)
        except Exception as e:
            print(e)
            return Response({'message': 'Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
def loginView(request):

    if request.method == 'POST':
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            if not email and not password:
                return Response({'error': 'Both username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

            user = authenticate(request, username=email, password=password)

            if not user:
                return Response({'message': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            if not user.is_email_verified:
                return Response({'message': 'Email not verified. Check your inbox or spam.'}, status=status.HTTP_401_UNAUTHORIZED)
            serializer = UserModelSerializer(user)
            token = get_tokens_for_user(user)
            login(request, user)
            return Response({'message': 'Login successful', 'user': serializer.data, 'token': token}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET'])
def logoutView(request):
    logout(request)
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


def activate_user(requestuest, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))

        user = get_object_or_404(User, pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        # messages.add_message(requestuest, messages.SUCCESS,
        #                      'Email verified, you can now login')
        return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)

    return Response({'message': 'Email not sent!'}, status=status.HTTP_501_NOT_IMPLEMENTED)


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [CustomAuthentication]
    queryset = User.objects.filter(is_superuser=False)
    serializer_class = UserModelSerializer
    parser_classes = [MultiPartParser, FormParser]

    # permission_classes = [CheckAuthenticatedUser]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=200)
