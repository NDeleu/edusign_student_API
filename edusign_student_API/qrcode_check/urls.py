from django.urls import path

from . import views

app_name = 'qr-code'

urlpatterns = [
    path('generate/', views.QRCodeGeneratorView.as_view(), name='generate_qr_code'),
]
