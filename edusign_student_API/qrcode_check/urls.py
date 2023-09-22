from django.urls import path

from . import views

app_name = 'qr-code'

urlpatterns = [
    # QRCode :
    path('generate/', views.QRCodeGeneratorView.as_view(), name='generate_qr_code'),
    path('validate/', views.ValidateQRCode.as_view(), name='validate_qr_code'),
]
