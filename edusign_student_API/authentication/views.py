from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAdministrator
from .serializers import UserRegisterSerializer, MyTokenObtainPairSerializer

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


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

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
