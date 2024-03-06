from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import UserRoles


# Create your views here.


class CustomLoginView(LoginView):
    template_name = 'login.html'  # Replace 'accounts/login.html' with the path to your login template

    def form_valid(self, form):
        # Custom logic to handle successful login
        # For example, you can redirect the user to a specific page
        print('Valid login attempt')
        return super().form_valid(form)

    def form_invalid(self, form):
        # Custom logic to handle invalid login
        # For example, you can log the failed login attempt
        print('Invalid login attempt')
        return super().form_invalid(form)


class CustomSignupView(CreateView):
    template_name = 'register.html'  # La plantilla de registro
    form_class = UserCreationForm  # El formulario de creación de usuario proporcionado por Django
    success_url = reverse_lazy('login')  # La URL a la que se redirigirá después del registro exitoso

    def form_valid(self, form):
        # Custom logic to handle successful registration
        # For example, you can log the registered user
        print('Valid registration attempt')
        return super().form_valid(form)

    def form_invalid(self, form):
        # Custom logic to handle invalid registration
        # For example, you can log the failed registration attempt
        print('Invalid registration attempt')
        print(form.errors.as_data())
        return super().form_invalid(form)


@method_decorator(login_required, name='dispatch')
class ListUsersView(ListView):
    model = User
    template_name = 'users.html'
    context_object_name = 'users'
    
    def get_queryset(self):
        return User.objects.all()
    
    def get_context_data(self, **kwargs):

        print('ListUsersView')

        context = super().get_context_data(**kwargs)
        context['user_roles'] = UserRoles.objects.all()
        context['users'] = User.objects.all()

        print(context['roles'])
        return context

