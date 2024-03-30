from django.shortcuts import render
from functools import wraps


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
