from django.http import HttpResponse
from django.contrib.auth import get_user_model
from rest_framework.viewsets import GenericViewSet

from users.tokens import account_activation_token
from .serializers import UserSerializer, PasswordResetSerializer, PasswordResetConfirm, \
    UserProfileSerializer, PasswordChangeSerializer
from rest_framework.generics import CreateAPIView, get_object_or_404, UpdateAPIView
from rest_framework import permissions, status, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

User = get_user_model()


class CreateUserView(CreateAPIView):
    model = User
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer


class PasswordResetView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = PasswordResetConfirm

    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            uid = serializer.data['uid']
            uid = force_text(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
            return Response('Password for {} has been succesfully changed'.format(user), status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def activate(request, uidb64, token, *args, **kwargs):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can log in to your account.')
    else:
        return HttpResponse('Activation link is invalid!')


class UserProfileViewSet(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


class PasswordChangeView(UpdateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = PasswordChangeSerializer

    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs.get('user_id'))

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            if not obj.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            obj.set_password(serializer.data.get("new_password"))
            obj.save()
            return Response('Password for {} has been succesfully changed'.format(obj),
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
