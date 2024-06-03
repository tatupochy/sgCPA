from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.views.generic import RedirectView
from django.contrib.auth.models import Group, Permission, User
from django.contrib.auth import login as auth_login
from cities.models import Cities
from countries.models import Country
from .models import User, Person, UserLogin
from .decorators import attribute_required, login_required_custom
from django.urls import reverse_lazy
from django.conf import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Create your views here.


class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        user = self.request.user
        user_logins = UserLogin.objects.filter(user=user).first()
        if user_logins.first_login:
            # Si es el primer inicio de sesión, redirige a la página de cambio de contraseña
            user_logins.first_login = False
            user_logins.save()
            return reverse_lazy('change_password', kwargs={'pk': user.pk})
        else:
            # De lo contrario, redirige a la URL personalizada después del inicio de sesión
            return reverse_lazy('listado_alumnos')
        
    def form_valid(self, form):
        print('Valid login attempt')

        user = User.objects.get(username=form.data['username'])

        if user.is_superuser:
            # add user to admin group
            group = Group.objects.get(name='Administrador')
            user.groups.add(group)
            user.save()

        user_logins = UserLogin.objects.filter(user=user)

        if user_logins.exists():
            user_login = user_logins.first()
            user_login.attempts = 0
            user_login.last_login = user.last_login
            user_login.save()
        else:
            user_login = UserLogin(user=user, attempts=0)
            user_login.save()

        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

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
                user.save()
                return render(self.request, "user_blocked.html")

            user_login.save()
        else:
            user_login = UserLogin(user=user, attempts=1)
            user_login.save()

        print('Invalid login attempt')
        return super().form_invalid(form)

        
class LogoutView(RedirectView):
    url = reverse_lazy('login')  # Redirige a la página de inicio de sesión después de cerrar sesión

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


@login_required_custom
def persons_view(request):
    persons = Person.objects.all()
    return render(request, "persons.html", {'persons': persons})


@attribute_required
@login_required_custom
def person_create_view(request):
    if request.method == "GET":
        
        users = User.objects.all()
        countries = Country.objects.all()
        cities = Cities.objects.all()

        return render(request, "person_create.html", {'users': users, 'countries': countries, 'cities': cities})
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
    

@login_required_custom
def person_detail_view(request, pk):
    person = get_object_or_404(Person, pk=pk)

    print("person birth_date", person.birth_date)
    formatted_birth_date = person.birth_date.strftime('%Y-%m-%d')
    person.birth_date = formatted_birth_date
    return render(request, "person_detail.html", {'person': person})


@attribute_required
@login_required_custom
def person_edit_view(request, pk):
    person = get_object_or_404(Person, pk=pk)
    countries = Country.objects.all()
    cities = Cities.objects.all()
    if request.method == "GET":
        # print json of person
        print("person", person.__dict__)
        return render(request, "person_edit.html", {'person': person, 'countries': countries, 'cities': cities})
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

        if person.user is not None:
            user = person.user
            user.email = form_data['email']
            user.first_name = form_data['name']
            user.last_name = form_data['last_name']
            user.save()

        person.save()
        return redirect('person_detail', pk=person.pk)


@login_required_custom
def users_view(request):
    # Obtén todos los usuarios activos por defecto
    users = User.objects.filter(is_active=True)

    # Verifica si el parámetro GET show_inactive_users está presente y es igual a "true"
    if request.GET.get('show_inactive_users') == 'true':
        # Si el filtro está activado, obtén todos los usuarios (activos e inactivos)
        users = User.objects.all()

    return render(request, "users.html", {'users': users})


@login_required_custom
def user_detail_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    person = Person.objects.filter(user=user).first()
    return render(request, "user_detail.html", {'user': user, 'person': person})


@attribute_required
@login_required_custom
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
        # user.username = form_data['username']
        # user.email = form_data['email']
        # user.first_name = form_data['first_name']
        # user.last_name = form_data['last_name']

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
@login_required_custom
def user_create_view(request):
    persons = Person.objects.all()
    roles = Group.objects.all()
    if request.method == "GET":
        return render(request, "user_create.html", {'persons': persons, 'groups': roles})
    else:
        form_data = request.POST.dict()
        print('form_data', form_data)

        password = form_data['password']

        # create user with person data
        person = Person.objects.get(pk=form_data['person'])
        if person.user:
            return render(request, "user_create.html", {'roles': roles, 'error': 'La persona ya tiene un usuario asociado', 'persons': persons})
        username = form_data['username']
        email = person.email
        first_name = person.name
        last_name = person.last_name
        password = form_data['password']
        user = User.objects.create_user(username = username, email = email, first_name = first_name, last_name = last_name, password = password, is_active=True)

        # send email to user
        send_mail('Bienvenido a sgCPA', 'Tu usuario ha sido creado', settings.EMAIL_HOST_USER, [email])

        person.user = user
        person.save()
        # asign group to user
        group = form_data['group']
        user.groups.add(group)

        return redirect('user_detail', pk=user.pk)


def send_mail(subject, message, from_email, recipient_list):

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ', '.join(recipient_list)
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, settings.EMAIL_HOST_PASSWORD)
    text = msg.as_string()
    server.sendmail(from_email, recipient_list, text)
    server.quit()


@attribute_required
@login_required_custom
def user_create_by_person_view(request, pk):
    person = get_object_or_404(Person, pk=pk)
    roles = Group.objects.all()
    if request.method == "GET":
        return render(request, "user_create_by_person.html", {'person': person, 'groups': roles})
    else:
        form_data = request.POST.dict()
        print('form_data', form_data)

        password = form_data['password']

        # create user with person data
        person = Person.objects.get(pk=pk)
        if person.user:
            return render(request, "user_create_by_person.html", {'roles': roles, 'error': 'La persona ya tiene un usuario asociado', 'person': person})
        username = form_data['username']
        email = person.email
        first_name = person.name
        last_name = person.last_name
        password = form_data['password']
        user = User.objects.create_user(username = username, email = email, first_name = first_name, last_name = last_name, password = password, is_active=True)

        # send email to user, bring .env variables
        send_mail('Bienvenido a sgCPA', 'Tu usuario ha sido creado', settings.EMAIL_HOST_USER, [email])

        person.user = user
        person.save()
        # asign group to user
        group = form_data['group']
        user.groups.add(group)

        return redirect('user_detail', pk=user.pk)

@attribute_required
@login_required_custom
def user_delete_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user == request.user:
        return render(request, "user_delete_error.html")
    else:
        user.is_active = False
        user.save()
    return redirect('users')


@login_required_custom
def change_password(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "GET":
        return render(request, "user_change_password.html", {'user': user})
    else:
        form_data = request.POST.dict()
        print('form_data', form_data)

        password = form_data['password']
        confirm_password = form_data['password2']

        if password != confirm_password:
            return render(request, "user_change_password.html", {'user': user, 'error': 'Las contraseñas no coinciden'})
        else:
            user.set_password(password)
            user.last_login = None
            user.save()

        return redirect('users')


@login_required_custom
def roles_view(request):
    roles = Group.objects.all()
    return render(request, "roles.html", {'roles': roles})


@login_required_custom
def role_detail_view(request, pk):
    role = get_object_or_404(Group, pk=pk)
    permissions = role.permissions.all()

    permissions_by_model = {}
    for permission in permissions:
        model_name = permission.content_type.model
        if model_name not in permissions_by_model:
            permissions_by_model[model_name] = []
        permissions_by_model[model_name].append(permission)

    return render(request, "role_detail.html", {'role': role, 'permissions': permissions, 'permissions_by_model': permissions_by_model})


@attribute_required
@login_required_custom
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
@login_required_custom
def role_edit_view(request, pk):
    role = get_object_or_404(Group, pk=pk)
    role_permissions = role.permissions.all()
    # filter all permissions that start with 'xyz_'
    permissions = Permission.objects.filter(codename__startswith='xyz_')

    # group permissions by model
    permissions_by_model = {}
    for permission in permissions:
        model_name = permission.content_type.model
        if model_name not in permissions_by_model:
            permissions_by_model[model_name] = []
        permissions_by_model[model_name].append(permission)

    # print('permissions_by_model', permissions_by_model)

    if request.method == "GET":
        return render(request, "role_edit.html", {'role': role, 'role_permissions': role_permissions, 'permissions': permissions, 'permissions_by_model': permissions_by_model})
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
@login_required_custom
def role_delete_view(request, pk):
    role = get_object_or_404(Group, pk=pk)
    role.delete()
    return redirect('roles')
