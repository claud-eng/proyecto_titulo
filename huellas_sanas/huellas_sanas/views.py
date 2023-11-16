from django.shortcuts import render
from django.conf import settings
import sendgrid
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import base64
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'base/home.html')

def enviar_consulta(request):
    if request.method == 'POST':
        # Obtén los datos del formulario
        correo_remitente = request.POST.get('correo')  # Dirección de correo del remitente
        asunto = request.POST.get('asunto')
        mensaje = request.POST.get('mensaje')

        # Construye el contenido del mensaje
        contenido_mensaje = f'Dirección de correo del remitente: {correo_remitente}\n\n'
        contenido_mensaje += f'Asunto: {asunto}\n\n'
        contenido_mensaje += f'Mensaje: {mensaje}'

        # Configura el cliente SendGrid
        sg = sendgrid.SendGridAPIClient(api_key=settings.EMAIL_HOST_PASSWORD)

        # Crea un objeto de correo electrónico
        from_email = 'huellassanas2023@gmail.com'
        to_email = 'huellassanas2023@gmail.com'
        subject = 'Consulta recibida'
        message = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject=subject,
            plain_text_content=contenido_mensaje
        )

        # Adjuntar imagen si está presente
        if 'archivo' in request.FILES:
            archivo = request.FILES['archivo']
            contenido_archivo = base64.b64encode(archivo.read()).decode()  # Codificar en base64 y decodificar a string
            adjunto = Attachment(
                FileContent(contenido_archivo),
                FileName(archivo.name),
                FileType(archivo.content_type),
                Disposition('attachment')
            )
            message.add_attachment(adjunto)

        # Envía el correo electrónico
        try:
            response = sg.send(message)
            return render(request, 'consulta_exitosa.html')  # Redirecciona a la página de consulta exitosa
        except Exception as e:
            print(str(e))  # Imprime el error en la consola para depurar
            return HttpResponse('Hubo un error al enviar el correo: ' + str(e))

    return render(request, 'consulta.html')

def consulta_exitosa(request):
    return render(request, 'consulta_exitosa.html')

def sobre_nosotros(request):
    return render(request, 'sobre_nosotros.html')

def preguntas_frecuentes(request):
    return render(request, 'preguntas_frecuentes.html')