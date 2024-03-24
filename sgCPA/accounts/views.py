from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import Group, Permission, User
from .models import User, Person, UserLogin
from .decorators import attribute_required


# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        print('Valid login attempt')

        user = User.objects.get(username=form.data['username'])
        user_logins = UserLogin.objects.filter(user=user)

        if user_logins.exists():
            user_login = user_logins.first()
            user_login.attempts = 0
            user_login.last_login = user.last_login
            user_login.save()
        else:
            user_login = UserLogin(user=user, attempts=0)
            user_login.save()

        return super().form_valid(form)

    def form_invalid(self, form):

        user = User.objects.get(username=form.data['username'])
        print('user', user)

        user_logins = UserLogin.objects.filter(user=user)
        if user_logins.exists():
            user_login = user_logins.first()
            user_login.attempts += 1

            if user_login.attempts >= 3:
                user.is_active = False
                user_login.attempts = 0
                user_login.save()
                return render(self.request, "login_error.html")

            user_login.save()
        else:
            user_login = UserLogin(user=user, attempts=1)
            user_login.save()

        print('Invalid login attempt')
        return super().form_invalid(form)


@login_required
def persons_view(request):
    persons = Person.objects.all()
    return render(request, "persons.html", {'persons': persons})


@attribute_required
@login_required
def person_create_view(request):
    if request.method == "GET":
        
        users = User.objects.all()

        return render(request, "person_create.html", {'users': users})
    else:
        form_data = request.POST.dict()
        print('form_data', form_data)

        person = Person(user=None,
                        name=form_data['name'],
                        last_name=form_data['last_name'],
                        email=form_data['email'],
                        phone=form_data['phone'],
                        address=form_data['address'],
                        city=form_data['city'],
                        country=form_data['country'],
                        postal_code=form_data['postal_code'],
                        birth_date=form_data['birth_date'])
        person.save()
        return redirect('person_detail', pk=person.pk)
    

@login_required
def person_detail_view(request, pk):
    person = get_object_or_404(Person, pk=pk)

    print("person birth_date", person.birth_date)
    formatted_birth_date = person.birth_date.strftime('%Y-%m-%d')
    person.birth_date = formatted_birth_date
    return render(request, "person_detail.html", {'person': person})


@attribute_required
@login_required
def person_edit_view(request, pk):
    person = get_object_or_404(Person, pk=pk)
    if request.method == "GET":
        # print json of person
        print("person", person.__dict__)
        return render(request, "person_edit.html", {'person': person})
    else:
        form_data = request.POST.dict()
        print('form_data', form_data)

        person.name = form_data['name']
        person.last_name = form_data['last_name']
        person.email = form_data['email']
        person.phone = form_data['phone']
        person.address = form_data['address']
        person.city = form_data['city']
        person.country = form_data['country']
        person.postal_code = form_data['postal_code']
        person.birth_date = form_data['birth_date']
        person.save()
        return redirect('person_detail', pk=person.pk)


@login_required
def users_view(request):
    users = User.objects.all()

    return render(request, "users.html", {'users': users})


@login_required
def user_detail_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    person = Person.objects.filter(user=user).first()
    return render(request, "user_detail.html", {'user': user, 'person': person})


@attribute_required
@login_required
def user_edit_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    groups = Group.objects.all()

    print("active user", user.is_active)
    print('user_is_active', user.is_active)

    print('request.method', request.method)

    if request.method == "GET":
        return render(request, "user_edit.html", {'user': user, 'groups': groups})
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

        # update user group
        group = form_data['group']
        user.groups.clear()
        user.groups.add(group)

        user.save()

        return redirect('users')


@attribute_required
@login_required
def user_create_view(request):
    persons = Person.objects.all()
    roles = Group.objects.all()
    if request.method == "GET":
        return render(request, "user_create.html", {'persons': persons, 'groups': roles})
    else:
        form_data = request.POST.dict()
        print('form_data', form_data)

        password = form_data['password']
        confirm_password = form_data['password2']

        if password != confirm_password:
            return render(request, "user_create.html", {'roles': roles, 'error': 'Las contraseñas no coinciden', 'persons': persons})
        else:
            # create user with person data
            person = Person.objects.get(pk=form_data['person'])
            if person.user:
                return render(request, "user_create.html", {'roles': roles, 'error': 'La persona ya tiene un usuario asociado', 'persons': persons})
            username = form_data['username']
            email = person.email
            first_name = person.name
            last_name = person.last_name
            password = form_data['password']
            user = User.objects.create_user(username = username, email = email, first_name = first_name, last_name = last_name, password = password)
            person.user = user
            person.save()
            # asign group to user
            group = form_data['group']
            user.groups.add(group)

        return redirect('user_detail', pk=user.pk)


@attribute_required
@login_required
def user_delete_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user == request.user:
        return render(request, "user_delete_error.html")
    else:
        user.delete()
    return redirect('users')


@login_required
def roles_view(request):
    roles = Group.objects.all()
    return render(request, "roles.html", {'roles': roles})


@login_required
def role_detail_view(request, pk):
    role = get_object_or_404(Group, pk=pk)
    permissions = role.permissions.all()
    return render(request, "role_detail.html", {'role': role, 'permissions': permissions})


@attribute_required
@login_required
def role_create_view(request):
    if request.method == "GET":
        return render(request, "role_create.html")
    else:
        form_data = request.POST.dict()
        print('form_data', form_data)

        role = Group(name=form_data['name'])
        role.save()

        return redirect('roles')


@attribute_required
@login_required
def role_edit_view(request, pk):
    role = get_object_or_404(Group, pk=pk)
    role_permissions = role.permissions.all()
    permissions = Permission.objects.all()
    if request.method == "GET":
        return render(request, "role_edit.html", {'role': role, 'role_permissions': role_permissions, 'permissions': permissions})
    else:
        form_data = request.POST.dict()
        print('form_data', form_data)

        role.name = form_data['name']
        role.permissions.clear()
        for key, value in form_data.items():
            if key.startswith('permission_'):
                permission = Permission.objects.get(pk=value)
                role.permissions.add(permission)
        
        role.save()
        return redirect('role_detail', pk=role.pk)
    

@attribute_required
@login_required
def role_delete_view(request, pk):
    role = get_object_or_404(Group, pk=pk)
    role.delete()
    return redirect('roles')
