from django.http import HttpResponse, HttpResponseBadRequest

from django.core.mail import send_mail

def sendEmail(subject, message, to_email):
    try:
        send_mail(subject, message, None,[to_email])
        return HttpResponse("Correo enviado correctamente")
    except Exception as e:
        error_message = str(e)
        return HttpResponseBadRequest(error_message)
