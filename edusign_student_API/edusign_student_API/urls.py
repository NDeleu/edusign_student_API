from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # Admin :
    path('admin/', admin.site.urls),
    
    # Include :
    path('api/auth/', include('authentication.urls')),
    path('api/lesson/', include('lessons.urls')),
    path('api/qr-code/', include('qrcode_check.urls')),
    path('api/justification/', include('justication_absence.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)