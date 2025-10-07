from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

from cukcuapp.views import healthz, home_check


# Health check view
def healthz(request):
    return JsonResponse({"status": "healthy"}, status=200)

urlpatterns = [
path('healthz/', healthz),
    path('', home_check, name='home_check'),
    path('admin/', admin.site.urls),
    path('', include('cukcuapp.urls')),

    path('healthz', healthz, name='healthz_no_slash'),  # Without slash
    path('health/', healthz, name='health'),  # Alternative path
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)