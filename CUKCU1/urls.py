from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

from cukcuapp.views import healthz


# Health check view
def healthz(request):
    return JsonResponse({"status": "healthy"}, status=200)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cukcuapp.urls')),
    path('healthz/', healthz, name='healthz'),
    path('healthz', healthz, name='healthz_no_slash'),  # Without slash
    path('health/', healthz, name='health'),  # Alternative path
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Catch-all for root health checks
handler400 = lambda request, exception=None: JsonResponse({"status": "bad_request"}, status=400)
handler404 = lambda request, exception=None: JsonResponse({"status": "not_found"}, status=404)
handler500 = lambda request, exception=None: JsonResponse({"status": "error"}, status=500)

