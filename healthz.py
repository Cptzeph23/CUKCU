from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

@csrf_exempt
@require_GET
def health_check(request):
    """
    Simple health check view that returns a 200 OK response.
    This is exempt from CSRF protection and only accepts GET requests.
    """
    return HttpResponse("OK", content_type="text/plain")