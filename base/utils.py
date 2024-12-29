from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import BadHeaderError
from django.http import HttpResponse

def enviar_correo(destinatario, asunto, mensaje):
    try:
        send_mail(
            asunto,  # Asunto del correo
            mensaje,  # Cuerpo del correo
            settings.EMAIL_HOST_USER,  # Remitente
            [destinatario],  # Lista de destinatarios
            fail_silently=False,
        )
    except BadHeaderError:
        return HttpResponse('Encabezado inválido encontrado.')
    except Exception as e:
        return HttpResponse(f'Error al enviar el correo: {str(e)}')
    