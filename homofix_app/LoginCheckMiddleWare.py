from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user
        # Allow access to API endpoints and authentication paths without authentication
        if request.path == "/" or request.path == "/Login/":
            return None
            
        allowed_paths = ["/api/", "/admin/", "/static/"]
        if any(request.path.startswith(path) for path in allowed_paths):
            return None

        # Redirect to login if user is not authenticated
        if not user.is_authenticated:
            return HttpResponseRedirect("/")

        # Define allowed modules for each user type
        user_modules = {
            "1": {  # HOD
                "allowed": ["homofix_app.HodViews", "homofix_app.views", "django.views.static", "django.contrib.admin"],
                "redirect": "admin_dashboard"
            },
            "2": {  # Technician
                "allowed": ["homofix_app.TechnicianViews", "homofix_app.views", "django.views.static"],
                "redirect": "technician_dashboard"
            },
            "3": {  # Support
                "allowed": ["homofix_app.SupportViews", "homofix_app.views", "django.views.static"],
                "redirect": "support_dashboard"
            },
            "4": {  # Customer
                "allowed": ["homofix_app.CustomerViews", "homofix_app.views", "django.views.static"],
                "redirect": "customer_dashboard"
            }
        }

        # Get user type configuration
        user_config = user_modules.get(user.user_type)
        if not user_config:
            return HttpResponseRedirect("/")

        # Check if current module is allowed for user type
        if modulename.startswith("django.contrib.admin") or \
           any(modulename == allowed for allowed in user_config["allowed"]):
            return None

        # Redirect to appropriate dashboard
        return HttpResponseRedirect(reverse(user_config["redirect"]))
