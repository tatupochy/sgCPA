from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .models import Role, User, UserRoles
from .decorators import attribute_required


# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        print('Valid login attempt')
        return super().form_valid(form)

    def form_invalid(self, form):
        print('Invalid login attempt')
        return super().form_invalid(form)


@login_required
def users_view(request):
    users = User.objects.all()

    for user in users:
        user_roles = UserRoles.objects.filter(user=user).first()
        if user_roles:
            user.role = user_roles.role
        else:
            user.role = None

    return render(request, "users.html", {'users': users})


@login_required
def user_detail_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    user_roles = UserRoles.objects.filter(user=user).first()
    if user_roles:
        user.role = user_roles.role
    return render(request, "user_detail.html", {'user': user})


@attribute_required
@login_required
def user_edit_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    roles = Role.objects.all()
    user_roles = UserRoles.objects.filter(user=user).first()

    print("active user", user.is_active)
    print("roles", roles)
    print("user_roles", user_roles)
    print('user_is_active', user.is_active)

    print('request.method', request.method)

    if request.method == "GET":
        return render(request, "user_edit.html", {'user': user, 'roles': roles, 'user_roles': user_roles})
    else:
        form_data = request.POST.dict()
        print('form_data', form_data)

        # update user
        user.username = form_data['username']
        user.email = form_data['email']
        user.first_name = form_data['first_name']
        user.last_name = form_data['last_name']

        if 'is_active' in form_data:
            if form_data['is_active'] == 'on':
                user.is_active = True
            else:
                user.is_active = False
        else:
            user.is_active = False

        user.save()

        # update user roles
        role = Role.objects.get(pk=form_data['role'])
        if user_roles:
            print("user_roles", user_roles)
            user_role = user_roles
            user_role.role = role
            user_role.save()
        else:
            user_role = UserRoles(user=user, role=role)
            user_role.save()

        return redirect('users')


@attribute_required
@login_required
def user_create_view(request):
    roles = Role.objects.all()
    if request.method == "GET":
        return render(request, "user_create.html", {'roles': roles})
    else:
        form_data = request.POST.dict()
        print('form_data', form_data)

        password = form_data['password']
        confirm_password = form_data['password2']

        if password != confirm_password:
            return render(request, "user_create.html", {'roles': roles, 'error': 'Passwords do not match'})
        else:
            # create user with hashed password
            user = User.objects.create_user(username=form_data['username'],
                                            email=form_data['email'],
                                            first_name=form_data['first_name'],
                                            last_name=form_data['last_name'],
                                            password=password)
            user.is_active = False  # set user as inactive
            user.save()

            # create user roles
            role = Role.objects.get(pk=form_data['role'])
            user_role = UserRoles(user=user, role=role)
            user_role.save()

        return redirect('users')


@attribute_required
@login_required
def user_delete_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user == request.user:
        return render(request, "user_delete_error.html")
    else:
        user.delete()
    return redirect('users')
