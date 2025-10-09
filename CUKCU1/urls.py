from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from healthz import health_check



urlpatterns = [
    path('admin/', admin.site.urls),
    path('healthz/', health_check, name='health_check'),
    path('', include('cukcuapp.urls')),
    path('healthz', health_check, name='healthz_no_slash'),  # Without slash
    path('health/', health_check, name='health'),  # Alternative path
]

# Serve media files in production
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)