from django.shortcuts import redirect
from django.urls import reverse, resolve


class LoginRequiredMiddleware:
    failed_url = reverse('account:login')
    exempt_urls_name = [
        'account:login'
    ]
    authenticated_urls_name = [
        'dashboard:index',
        'dashboard:settings',
        'dashboard:profile',
        'dashboard:profile-edit',
        'dashboard:category:index',
        'dashboard:category:create',
        'dashboard:category:update',
        'dashboard:category:delete',
        'dashboard:post:index',
        'dashboard:post:create',
        'dashboard:post:update',
        'dashboard:post:delete',
        'dashboard:comments',
        'dashboard:comment-delete',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if any(resolve(request.path_info).view_name == name for name in self.authenticated_urls_name):
            if not request.user.is_authenticated:
                return redirect(self.failed_url)
            else:
                if not request.user.is_active:
                    return redirect(self.failed_url)
                return None

        elif any(resolve(request.path_info).view_name == name for name in self.exempt_urls_name):
            if request.user.is_authenticated:
                return redirect(reverse('dashboard:index'))
        return None


class AdminRequiredMiddleware:
    failed_url = reverse('dashboard:index')
    authentication_urls_name = [
        'dashboard:settings',
        'dashboard:category:index',
        'dashboard:category:create',
        'dashboard:category:update',
        'dashboard:category:delete'
    ]

    def __init__(self, get_response):
        self.response = get_response

    def __call__(self, request):
        return self.response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if any(resolve(request.path_info).view_name == name for name in self.authentication_urls_name):
            if request.user.is_authenticated:
                if not request.user.is_admin:
                    return redirect(self.failed_url)

