from django import forms
from .models import Course

# class CursoForm(forms.ModelForm):
#     class Meta:
#         model = Course
#         fields = '__all__'


class CursoForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        labels = {
            'name': 'Nombre del curso',
            'start_date': 'Fecha de inicio',
            'end_date': 'Fecha de fin',
            'fee_amount': 'Monto cuota mensual',
            'days_per_week': 'Días por semana',
            'active': 'Curso activo?',
            'shift': 'Turno',
            'section': 'Sección',
            'year': 'Año',
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_fee_amount(self):
        fee_amount = self.cleaned_data['fee_amount']
        if fee_amount < 0:
            raise forms.ValidationError("El monto de la cuota mensual no puede ser negativo.")
        return fee_amount

    def clean_days_per_week(self):
        days_per_week = self.cleaned_data['days_per_week']
        if days_per_week <= 0:
            raise forms.ValidationError("Los días por semana deben ser un número positivo.")
        return days_per_week