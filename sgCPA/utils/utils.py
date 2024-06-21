from django.http import HttpResponse, HttpResponseBadRequest

from django.core.mail import send_mail
import datetime

def sendEmail(subject, message, to_email):
    try:
        send_mail(subject, message, None,[to_email])
        return HttpResponse("Correo enviado correctamente")
    except Exception as e:
        error_message = str(e)
        return HttpResponseBadRequest(error_message)


def calculate_class_days(start_date, end_date, class_days):
    """
    Calcula la cantidad de días de clase y las fechas de cada clase entre start_date y end_date.

    Args:
        start_date (datetime.date): Fecha de inicio del curso.
        end_date (datetime.date): Fecha de fin del curso.
        class_days (list[int]): Lista de enteros que representan los días de clase (1 para lunes, 2 para martes, etc.).

    Returns:
        tuple: (int, list[datetime.date]) - Cantidad total de días de clase y lista de fechas de clase.
    """
    # Convierte la lista de días de clase a un conjunto para una búsqueda más rápida
    class_days_set = set(class_days)

    # Inicializa el contador de días de clase y la lista de fechas de clase
    total_class_days = 0
    class_dates = []

    # Itera sobre cada día en el rango de fechas
    current_date = start_date
    while current_date <= end_date:
        if current_date.isoweekday() in class_days_set:
            total_class_days += 1
            class_dates.append(current_date)
        current_date += datetime.timedelta(days=1)

    return total_class_days, class_dates