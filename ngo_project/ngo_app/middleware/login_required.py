from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    """
    Middleware that requires user to be authenticated to access any page.
    Redirects to login page if not authenticated.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # URLs that don't require authentication
        self.exempt_urls = [
            '/accounts/login/',
            '/register/',
            '/admin/',
        ]

    def __call__(self, request):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            # Check if the current path is exempt
            path = request.path_info
            if not any(path.startswith(url) for url in self.exempt_urls):
                # Redirect to login with next parameter
                return redirect(f"{reverse('login')}?next={request.path}")

        response = self.get_response(request)
        return response