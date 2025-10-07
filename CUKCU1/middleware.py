class HealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if this is a health check request
        if request.path.strip('/') in ['healthz', 'health']:
            # Return a simple 200 OK response
            from django.http import HttpResponse
            return HttpResponse("OK", content_type="text/plain")
        
        # Process other requests normally
        return self.get_response(request)