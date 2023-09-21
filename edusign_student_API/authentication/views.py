from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView

from .permissions import IsAdministrator, IsAdministratorOrIntervening
from .serializers import (UserRegisterSerializer, UserListSerializer, UserDetailSerializer, 
                          UserDetailForUserSerializer, UserUpdateSerializer, PromotionCreateSerializer, 
                          PromotionListSerializer, PromotionDetailSerializer, PromotionUpdateSerializer, 
                          MyTokenObtainPairSerializer, Promotion) 

User = get_user_model()

# CRUD User :

class RegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (IsAuthenticated, IsAdministrator,)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            response.data = {
                "details": "User registered successfully",
                "user": response.data
            }
        return response
    
class UserListView(ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsAdministratorOrIntervening,)

class UserDetailView(RetrieveAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsAdministratorOrIntervening,)
    lookup_field = 'id'

class UserDetailForUserView(RetrieveAPIView):
    serializer_class = UserDetailForUserSerializer
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    lookup_field = 'id'

    def get_object(self):
        return self.request.user

class UserUpdateView(RetrieveUpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = (IsAuthenticated, IsAdministrator,)
    queryset = User.objects.all()
    lookup_field = 'id'

class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        if not user.check_password(current_password):
            return Response({"error": "Current password does not match"}, status=HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"message": "Password successfully updated!"}, status=HTTP_200_OK)

class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsAdministrator,)
    lookup_field = 'id'

# CRUD Promotion :

class PromotionCreateView(CreateAPIView):
    serializer_class = PromotionCreateSerializer
    permission_classes = (IsAuthenticated, IsAdministrator,)

class PromotionListView(ListAPIView):
    serializer_class = PromotionListSerializer
    queryset = Promotion.objects.all()
    permission_classes = (IsAuthenticated, IsAdministratorOrIntervening,)

class PromotionDetailView(RetrieveAPIView):
    serializer_class = PromotionDetailSerializer
    queryset = Promotion.objects.all()
    permission_classes = (IsAuthenticated, IsAdministratorOrIntervening,)
    lookup_field = 'id'

class PromotionUpdateView(RetrieveUpdateAPIView):
    serializer_class = PromotionUpdateSerializer
    queryset = Promotion.objects.all()
    permission_classes = (IsAuthenticated, IsAdministrator,)
    lookup_field = 'id'
    
class PromotionDeleteView(DestroyAPIView):
    queryset = Promotion.objects.all()
    permission_classes = (IsAuthenticated, IsAdministrator,)
    lookup_field = 'id'

# Token :

class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


