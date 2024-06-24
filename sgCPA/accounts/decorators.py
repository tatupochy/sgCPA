from django.shortcuts import render
from functools import wraps
from django.http import HttpResponseForbidden


def attribute_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, "unauthenticated.html")

        user = request.user
        user_group = user.groups.all()
        user_group_names = [group.name for group in user_group]

        if 'Administrador' not in user_group_names:
            return render(request, "unauthorized.html")

        return view_func(request, *args, **kwargs)

    return _wrapped_view

def login_required_custom(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, "unauthenticated.html")

        return view_func(request, *args, **kwargs)

    return _wrapped_view


def admin_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.groups.filter(name='Administrador').exists():
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    return _wrapped_view_func