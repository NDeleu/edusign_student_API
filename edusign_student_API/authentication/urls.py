from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'authentication'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('token/', views.EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/<int:id>/', views.UserDetailView.as_view(), name='user_detail'),
    path('users/my-details/', views.UserDetailForUserView.as_view(), name='my_details'),
    path('users/update/<int:id>/', views.UserUpdateView.as_view(), name='user_update'),
    path('users/change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('users/delete/<int:id>/', views.UserDeleteView.as_view(), name='user_delete'),
    path('promo/create/', views.PromotionCreateView.as_view(), name='promotion_create'),
    path('promo/', views.PromotionListView.as_view(), name='promotion_list'),
    path('promo/<int:id>/', views.PromotionDetailView.as_view(), name='promotion_details'),
    path('promo/update/<int:id>/', views.PromotionUpdateView.as_view(), name='promotion_update'),
    path('promo/delete/<int:id>/', views.PromotionDeleteView.as_view(), name='promotion_delete'),
]
