from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import UserRoles

class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email', 'first_name', 'last_name')


class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username','email', 'first_name', 'last_name')

    user_roles = forms.ModelMultipleChoiceField(queryset=UserRoles.objects.all(), required=False)


class UserRolesForm(forms.ModelForm):
    class Meta:
        model = UserRoles
        fields = ('user', 'role')
