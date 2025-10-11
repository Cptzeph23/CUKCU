from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin
import os
from datetime import datetime, timedelta, timezone
import datetime
from django.conf import settings
from django.shortcuts import render
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

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

class ComingSoonMiddleware(MiddlewareMixin):
    """
    Displays a 'Coming Soon' page for all users until the launch date/time.
    Automatically disables COMING_SOON_ENABLED once launch time is reached.
    """

    def process_request(self, request):
        # Allow admin/staff and admin panel to bypass
        if request.user.is_authenticated and request.user.is_staff:
            return None
        if request.path.startswith("/admin"):
            return None

        # Check if COMING_SOON is enabled
        if getattr(settings, "COMING_SOON_ENABLED", False):
            launch_str = getattr(settings, "COMING_SOON_LAUNCH_DATETIME", None)

            if launch_str:
                try:
                    launch_time = datetime.datetime.fromisoformat(launch_str)
                except Exception:
                    launch_time = timezone.now()

                now = timezone.localtime(timezone.now())

                # If it's launch time or later — disable Coming Soon automatically
                if now >= launch_time:
                    os.environ["COMING_SOON_ENABLED"] = "False"
                    settings.COMING_SOON_ENABLED = False
                    return None

                # Otherwise, render Coming Soon page
                remaining_time = launch_time - now
                days = remaining_time.days
                hours, remainder = divmod(remaining_time.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)

                return render(
                    request,
                    "coming_soon.html",
                    {
                        "days": days,
                        "hours": hours,
                        "minutes": minutes,
                        "seconds": seconds,
                        "launch_datetime": launch_time.isoformat(),
                    },
                )

        return None