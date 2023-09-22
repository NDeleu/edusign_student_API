from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # Admin :
    path('admin/', admin.site.urls),
    
    # Include :
    path('api/auth/', include('authentication.urls')),
    path('api/lesson/', include('lesson.urls')),
    path('api/qr-code/', include('qr-code.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)