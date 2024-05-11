from django.shortcuts import redirect

class AuthenticationMiddleware:
    def _init_(self, get_response):
        self.get_response = get_response

    def _call_(self, request):
        if not request.user.is_authenticated and not request.path_info.startswith('/login'):
            return redirect('login')  # Redirect to login page
        return self.get_response(request)