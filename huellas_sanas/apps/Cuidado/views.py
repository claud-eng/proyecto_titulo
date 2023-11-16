from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Ficha
from .forms import FichaForm
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from apps.Cita.models import Mascota
from apps.Usuario.models import Cliente 
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from .models import Ficha
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import io 

@login_required
def listar_fichas(request):
    # Vista para listar fichas con opciones de búsqueda y paginación

    # Obtener el usuario actualmente logeado
    user = request.user

    # Inicializar la variable de consulta para todas las fichas
    fichas = Ficha.objects.all()

    # Obtener el valor de búsqueda del parámetro 'mascota' en la URL
    mascota_query = request.GET.get('mascota')

    if user.is_authenticated:
        # Si el usuario está autenticado

        # Si el usuario es un Cliente, filtrar fichas por sus mascotas
        if hasattr(user, 'cliente'):
            fichas = fichas.filter(mascota__cliente=user.cliente)
        elif user.empleado and user.empleado.rol == 'Veterinario':
            # Si el usuario es un Empleado con el rol de Veterinario, no aplicar ningún filtro
            pass
        else:
            # Otros usuarios no permitidos, redireccionar o mostrar un mensaje de error según sea necesario
            # Puedes personalizar esto de acuerdo a tus requerimientos
            return HttpResponse("Acceso no autorizado")

        # Si se proporcionó un valor de búsqueda de mascota, filtrar fichas por mascota
        if mascota_query:
            fichas = fichas.filter(mascota__nombre__icontains=mascota_query)

        # Configurar la paginación
        paginator = Paginator(fichas, 5)  # Mostrar 5 fichas por página
        page = request.GET.get('page')  # Obtener el número de página de la solicitud GET

        try:
            fichas = paginator.page(page)
        except PageNotAnInteger:
            fichas = paginator.page(1)  # Si la página no es un número entero, mostrar la primera página
        except EmptyPage:
            fichas = paginator.page(paginator.num_pages)  # Si la página está fuera de rango, mostrar la última página

        # Agregar una variable de contexto para indicar si se ha realizado una búsqueda
        has_search_query_mascota = bool(mascota_query)
    else:
        # Si el usuario no está autenticado, puedes redirigirlo a la página de inicio de sesión o mostrar un mensaje de error
        # Puedes personalizar esto según tus necesidades
        return HttpResponse("Acceso no autorizado")

    return render(request, 'Cuidado/listar_fichas.html', {
        'fichas': fichas,
        'has_search_query_mascota': has_search_query_mascota,
    })

@login_required
def generar_ficha_pdf(request, id_ficha):
    ficha = Ficha.objects.get(id=id_ficha)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ficha_medica_{id_ficha}.pdf"'

    buffer = io.BytesIO()
    
    # Creamos un documento PDF con el buffer como su "archivo"
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)

    # Creamos un arreglo de 'Flowables' para agregar al documento
    flowables = []

    # Obtenemos el estilo de ReportLab y creamos estilos para los párrafos
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=1))

    # Agregamos los datos de la ficha
    flowables.append(Paragraph(f"Empresa: Huellas Sanas S.A."))
    flowables.append(Paragraph(f"Cliente: {ficha.cliente.user.username}", styles['Normal']))
    flowables.append(Paragraph(f"Mascota: {ficha.mascota.nombre}", styles['Normal']))
    flowables.append(Paragraph(f"Veterinario: {ficha.veterinario.user.get_full_name()}", styles['Normal']))
    flowables.append(Paragraph(f"Fecha: {ficha.fecha.strftime('%d/%m/%Y')}", styles['Normal']))
    flowables.append(Paragraph(f"Medicamento: {ficha.medicamento}", styles['Normal']))
    flowables.append(Paragraph(f"Dosis: {ficha.dosis}", styles['Normal']))
    flowables.append(Spacer(1, 12))
    flowables.append(Paragraph(f"Instrucciones:", styles['Normal']))
    flowables.append(Paragraph(f"{ficha.instrucciones}", styles['Justify']))

    # Construimos el documento con los flowables
    doc.build(flowables)

    # Movemos el valor del buffer al response para que se descargue el archivo PDF
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

@login_required
def agregar_ficha(request):
    if request.method == "POST":
        form = FichaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ficha agregada con éxito.')
            return redirect('listar_fichas')
    else:
        form = FichaForm()

    return render(request, "Cuidado/agregar_ficha.html", {'form': form})

def verificar_cliente_ficha(request):
    username = request.GET.get('username')
    try:
        cliente = Cliente.objects.get(user__username=username)
        mascotas = Mascota.objects.filter(cliente=cliente)
        mascotas_data = [{'id': mascota.id, 'nombre': mascota.nombre} for mascota in mascotas]
        return JsonResponse({'mascotas': mascotas_data, 'existe': True})
    except Cliente.DoesNotExist:
        return JsonResponse({'existe': False})
    
@login_required
def editar_ficha(request, ficha_id):
    instancia = Ficha.objects.get(id=ficha_id)

    if request.method == "POST":
        form = FichaForm(request.POST, instance=instancia, exclude_fields=['cliente_username', 'cliente', 'veterinario', 'mascota'])
        if form.is_valid():
            form.save()
            messages.success(request, 'Ficha editada con éxito.')
            return redirect('listar_fichas')
    else:
        fecha_actual = instancia.fecha.strftime('%Y-%m-%d')
        form = FichaForm(instance=instancia, initial={'fecha': fecha_actual}, exclude_fields=['cliente_username', 'cliente', 'veterinario', 'mascota'])

    return render(request, "Cuidado/editar_ficha.html", {'form': form})

@login_required
def confirmar_borrar_ficha(request, ficha_id):
    # Vista para confirmar la eliminación de una ficha

    ficha = Ficha.objects.get(id=ficha_id)
    return render(request, 'Cuidado/confirmar_borrar_ficha.html', {'ficha': ficha})

@login_required
def borrar_ficha(request, ficha_id):
    # Vista para borrar una ficha existente

    try:
        instancia = Ficha.objects.get(id=ficha_id)
        instancia.delete()
        messages.success(request, 'Ficha eliminada con éxito.')  # Agrega mensaje de éxito
    except Ficha.DoesNotExist:
        pass  # Manejar la situación en la que la ficha no existe

    return redirect('listar_fichas')  # Redirige a la lista de fichas después de borrar una

