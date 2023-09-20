from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenRefreshView
from authentication.views import RegisterView, EmailTokenObtainPairView, ChangePasswordView, UserListView, UserDetailView, UserDetailForUserView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/token/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('api/user/change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('api/users/', UserListView.as_view(), name='user_list'),
    path('api/users/<int:id>/', UserDetailView.as_view(), name='user_detail'),
    path('api/users/my-details/', UserDetailForUserView.as_view(), name='my_details'),
]
