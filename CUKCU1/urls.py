from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from cukcuapp.views import home_check


# Health check view for Render
@csrf_exempt
def health_check(request):
    return HttpResponse("OK", status=200)

urlpatterns = [
    path('healthz/', health_check, name='health_check'),
    path('', home_check, name='home_check'),
    path('admin/', admin.site.urls),
    path('', include('cukcuapp.urls')),
    path('healthz', health_check, name='healthz_no_slash'),  # Without slash
    path('health/', health_check, name='health'),  # Alternative path
]

# Serve media files in production
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)