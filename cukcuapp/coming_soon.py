
import os
from datetime import datetime, timezone as dt_timezone
from django.conf import settings
from django.shortcuts import render
from django.utils import timezone
from django.utils.dateparse import parse_datetime


def _env_flag_true(val):
    return str(val).lower() in ("1", "true", "yes", "on")


class ComingSoonMiddleware:
    """
    If enabled and now < launch_at, render a coming_soon page (HTTP 503).
    Whitelisted paths (static, media, admin login, healthz, robots, sitemap)
    are allowed through. Staff users (is_staff) and preview query param bypass.
    """

    def __init__(self, get_response):
        self.get_response = get_response

        # prefer Django setting if provided, otherwise environment
        self.enabled = getattr(settings, "COMING_SOON_ENABLED", None)
        if self.enabled is None:
            self.enabled = _env_flag_true(os.environ.get("COMING_SOON_ENABLED", "False"))

        # Launch time: prefer Django setting string/datetime, otherwise env var
        launch_val = getattr(settings, "COMING_SOON_LAUNCH_AT", None) or os.environ.get(
            "COMING_SOON_LAUNCH_AT"
        )

        self.launch_at = None
        if launch_val:
            # if it's already a datetime in settings, accept it
            if isinstance(launch_val, datetime):
                self.launch_at = launch_val
            else:
                # parse ISO-ish string
                dt = parse_datetime(str(launch_val).strip())
                if dt is None:
                    # fallback: attempt simple fromisoformat (Python 3.11+)
                    try:
                        dt = datetime.fromisoformat(str(launch_val).strip())
                    except Exception:
                        dt = None
                if dt:
                    if timezone.is_naive(dt):
                        # assume UTC if timezone missing
                        dt = dt.replace(tzinfo=dt_timezone.utc)
                    self.launch_at = dt.astimezone(timezone.get_default_timezone())

        # Paths to always allow through (prefix match)
        self.ALLOWED_PATH_PREFIXES = (
            "/static/",
            "/media/",
            "/favicon.ico",
            "/robots.txt",
            "/sitemap.xml",
            "/healthz",
        )

        # Exact allowed paths
        self.ALLOWED_PATHS = ("/",)  # we will treat root specially: usually blocked

    def _is_whitelisted(self, path: str) -> bool:
        # allow static/media/robots/sitemap and health checks
        for pfx in self.ALLOWED_PATH_PREFIXES:
            if path.startswith(pfx):
                return True
        return False

    def __call__(self, request):
        # if disabled or no launch time configured, pass through
        if not self.enabled or not self.launch_at:
            return self.get_response(request)

        # allow whitelisted paths (static, health, sitemap, robots)
        path = request.path
        if self._is_whitelisted(path):
            return self.get_response(request)

        # Allow staff users / admins to preview (requires AuthenticationMiddleware earlier)
        try:
            user = getattr(request, "user", None)
            if user and user.is_authenticated and getattr(user, "is_staff", False):
                return self.get_response(request)
        except Exception:
            # if anything goes wrong here, don't crash — fallback to blocking
            pass

        # Allow preview via query param ?preview=1 (handy for testing)
        if request.GET.get("preview") in ("1", "true", "on"):
            return self.get_response(request)

        # If now >= launch_at, allow normal site
        now = timezone.now()
        if now >= self.launch_at:
            return self.get_response(request)

        # At this point: show coming soon page
        seconds_left = int((self.launch_at - now).total_seconds())
        # Cap to minimum 0
        if seconds_left < 0:
            seconds_left = 0

        context = {
            "launch_at_iso": self.launch_at.astimezone(dt_timezone.utc).isoformat().replace("+00:00", "Z"),
            "seconds_left": seconds_left,
        }

        # Render the template (create templates/coming_soon.html)
        response = render(request, "coming_soon.html", context=context, status=503)
        # Optional: set Retry-After header (in seconds)
        response["Retry-After"] = str(seconds_left)
        return response
