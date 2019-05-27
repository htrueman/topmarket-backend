from django.http import HttpResponse
from django.contrib.auth import get_user_model
from rest_framework.viewsets import GenericViewSet
from users.permissions import IsOwner, IsPartner
from users.tasks import send_user_email
from users.tokens import account_activation_token
from .serializers import UserSerializer, PasswordResetSerializer, UserProfileSerializer, PasswordChangeSerializer,\
    CompanyUpdateSerializer, DocumentSerializer, CompanyPitchSerializer, MyStoreSerializer, ManagerSerializer, \
    ActivityAreasSerializer, ServiceIndustrySerializer, CompanyTypeSerializer, CompanyRetrieveSerializer
from .models import Company, CompanyPitch, MyStore, ActivityAreas, ServiceIndustry, CompanyType
from rest_framework.generics import CreateAPIView, get_object_or_404, UpdateAPIView
from rest_framework import permissions, status, mixins, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import TokenObtainPairCustomSerializer


User = get_user_model()


class TokenObtainPairCustomView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = TokenObtainPairCustomSerializer


class CreateUserView(CreateAPIView):
    model = User
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PasswordResetView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        serializer.save()

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
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
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PasswordChangeSerializer

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.id)

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


class CompanyRetrieveView(generics.RetrieveAPIView):
    serializer_class = CompanyRetrieveSerializer
    permission_classes = [IsOwner, ]

    def get_object(self):
        obj, created = Company.objects.get_or_create(user=self.request.user)
        return obj


class CompanyUpdateView(generics.UpdateAPIView):
    serializer_class = CompanyUpdateSerializer
    permission_classes = [IsOwner, ]

    def get_object(self):
        obj, created = Company.objects.get_or_create(user=self.request.user)
        return obj


class DocumentSerializerRUView(generics.RetrieveUpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsOwner, ]

    def get_object(self):
        obj, created = Company.objects.get_or_create(user=self.request.user)
        return obj


class CompanyPitchRUView(generics.RetrieveUpdateAPIView):
    queryset = CompanyPitch.objects.all()
    serializer_class = CompanyPitchSerializer
    permission_classes = [IsOwner, ]

    def get_object(self):
        company = get_object_or_404(Company, user=self.request.user)
        obj, created = CompanyPitch.objects.get_or_create(company=company)
        return obj


class MyStoreRUView(generics.RetrieveUpdateAPIView):
    queryset = MyStore.objects.all()
    serializer_class = MyStoreSerializer
    permission_classes = [IsOwner, ]

    def get_object(self):
        obj, created = MyStore.objects.get_or_create(user=self.request.user)
        return obj


class ManagerCreateView(CreateAPIView):
    model = User
    permission_classes = (IsPartner,)
    serializer_class = ManagerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ActivityAreasListCreateView(generics.ListCreateAPIView):
    queryset = ActivityAreas.objects.all()
    serializer_class = ActivityAreasSerializer
    permission_classes = [permissions.IsAuthenticated, ]


class ActivityAreasUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ActivityAreas.objects.all()
    serializer_class = ActivityAreasSerializer
    permission_classes = [permissions.IsAdminUser, ]


class ServiceIndustryListCreateView(generics.ListCreateAPIView):
    queryset = ServiceIndustry.objects.all()
    serializer_class = ServiceIndustrySerializer
    permission_classes = [permissions.IsAuthenticated, ]


class ServiceIndustryUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceIndustry.objects.all()
    serializer_class = ServiceIndustrySerializer
    permission_classes = [permissions.IsAdminUser, ]


class CompanyTypeListCreateView(generics.ListCreateAPIView):
    queryset = CompanyType.objects.all()
    serializer_class = CompanyTypeSerializer
    permission_classes = [permissions.IsAuthenticated, ]


class CompanyTypeUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CompanyType.objects.all()
    serializer_class = CompanyTypeSerializer
    permission_classes = [permissions.IsAdminUser, ]


class SendUserEmailAboutMissPhone(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, *args, **kwargs):
        send_user_email()
        return Response(status=status.HTTP_200_OK)
