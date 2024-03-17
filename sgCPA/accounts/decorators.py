from django.shortcuts import render
from .models import UserRoles
from functools import wraps


def attribute_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, "unauthenticated.html")
        
        user = request.user
        user_roles = UserRoles.objects.filter(user=user).first()
        if user_roles:
            user.role = user_roles.role
        else:
            user.role = None

        if user.role and user.role.name == 'user':
            return render(request, "unauthorized.html")

        return view_func(request, *args, **kwargs)

    return _wrapped_view
