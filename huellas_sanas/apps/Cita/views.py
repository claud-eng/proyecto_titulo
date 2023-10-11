from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Cita, Mascota
from apps.Cita.models import Cita, Mascota
from .forms import CitaForm, EditarCitaForm, MascotaForm, EditarMascotaForm
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required

@login_required
def listar_citas(request):
    # Vista para listar citas con opciones de búsqueda y paginación

    # Obtener el usuario actualmente logeado
    user = request.user

    # Inicializar la variable de consulta para todas las citas
    citas = Cita.objects.all()

    # Obtener los valores de búsqueda de los parámetros 'cliente' y 'veterinario' en la URL
    cliente_query = request.GET.get('cliente')
    veterinario_query = request.GET.get('veterinario')

    if user.is_authenticated:
        # Si el usuario está autenticado

        # Si el usuario es un Cliente, filtrar citas por su cuenta
        if hasattr(user, 'cliente'):
            citas = citas.filter(cliente=user.cliente)
        elif user.empleado and user.empleado.rol == 'Recepcionista':
            # Si el usuario es un Empleado con el rol de Recepcionista, no aplicar ningún filtro
            pass
        else:
            # Otros usuarios no permitidos, redireccionar o mostrar un mensaje de error según sea necesario
            # Puedes personalizar esto de acuerdo a tus requerimientos
            return HttpResponse("Acceso no autorizado")

        # Si se proporcionó un valor de búsqueda de cliente, filtrar citas por cliente
        if cliente_query:
            citas = citas.filter(cliente__user__username__icontains=cliente_query)

        # Si se proporcionó un valor de búsqueda de veterinario, filtrar citas por veterinario
        if veterinario_query:
            citas = citas.filter(veterinario__user__username__icontains=veterinario_query)

        # Configurar la paginación
        paginator = Paginator(citas, 5)  # Mostrar 5 citas por página
        page = request.GET.get('page')  # Obtener el número de página de la solicitud GET

        try:
            citas = paginator.page(page)
        except PageNotAnInteger:
            citas = paginator.page(1)  # Si la página no es un número entero, mostrar la primera página
        except EmptyPage:
            citas = paginator.page(paginator.num_pages)  # Si la página está fuera de rango, mostrar la última página

        # Agregar variables de contexto para indicar si se ha realizado una búsqueda
        has_search_query_cliente = bool(cliente_query)
        has_search_query_veterinario = bool(veterinario_query)
    else:
        # Si el usuario no está autenticado, puedes redirigirlo a la página de inicio de sesión o mostrar un mensaje de error
        # Puedes personalizar esto según tus necesidades
        return HttpResponse("Acceso no autorizado")

    return render(request, 'Cita/listar_citas.html', {
        'citas': citas,
        'has_search_query_cliente': has_search_query_cliente,
        'has_search_query_veterinario': has_search_query_veterinario,
    })

@login_required
def agendar_cita(request):
    # Vista para agregar una nueva cita desde un formulario

    # Obtener el usuario actualmente logeado
    user = request.user

    # Verificar si el usuario tiene el rol de recepcionista
    if user.is_authenticated:
        if hasattr(user, 'empleado') and user.empleado.rol == 'Recepcionista':
            # Si es un empleado con rol de Recepcionista, permitirle agregar una cita para cualquier cliente
            if request.method == "POST":
                form = CitaForm(request.POST, user=user)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Cita agendada con éxito.')
                    return redirect('listar_citas')
            else:
                form = CitaForm()
        elif hasattr(user, 'cliente'):
            # Si es un cliente, permitirle agregar una mascota solo para sí mismo
            if request.method == "POST":
                form = CitaForm(request.POST, user=user)  # Pasa el usuario actual al formulario
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Cita agendada con éxito.')
                    return redirect('listar_citas')
            else:
                form = CitaForm(user=user)  # Pasa el usuario actual al formulario
        else:
            # Otros usuarios no permitidos, redireccionar o mostrar un mensaje de error según sea necesario
            # Puedes personalizar esto de acuerdo a tus requerimientos
            return HttpResponse("Acceso no autorizado")
    else:
        # Si el usuario no está autenticado, puedes redirigirlo a la página de inicio de sesión o mostrar un mensaje de error
        # Puedes personalizar esto según tus necesidades
        return HttpResponse("Acceso no autorizado")

    return render(request, "Cita/agendar_cita.html", {'form': form})

def agendar_cita_sin_login(request):
    return render(request, 'Cita/agendar_cita_sin_login.html')

@login_required
def confirmar_borrar_cita(request, cita_id):
    # Vista para confirmar la eliminación de una cita

    cita = Cita.objects.get(id=cita_id)
    return render(request, 'Cita/confirmar_borrar_cita.html', {'cita': cita})

@login_required
def borrar_cita(request, cita_id):
    # Vista para borrar una cita existente

    try:
        instancia = Cita.objects.get(id=cita_id)
        instancia.delete()
        messages.success(request, 'Cita eliminada con éxito.')  # Agrega mensaje de éxito
    except Cita.DoesNotExist:
        pass  # Manejar la situación en la que la cita no existe

    return redirect('listar_citas')  # Redirige a la lista de citas después de borrar

@login_required
def confirmar_cancelar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)

    if request.method == "POST":
        # Cambiar el estado de la cita a "Cancelada"
        cita.estado = 'Cancelada'
        cita.save()
        messages.success(request, 'Cita cancelada con éxito.')  # Agrega mensaje de éxito
        return redirect('listar_citas')  # Redirige a la lista de citas después de cancelar la cita

    return render(request, 'Cita/confirmar_cancelar_cita.html', {'cita': cita})

@login_required
def editar_cita(request, cita_id):
    # Vista para editar la información de una cita existente

    instancia = Cita.objects.get(id=cita_id)

    if request.method == "POST":
        form = EditarCitaForm(request.POST, instance=instancia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cita editada con éxito.')
            return redirect('listar_citas')
    else:
        # Obtener los valores actuales de fecha y hora y convertirlos a cadenas
        fecha_actual = instancia.fecha.strftime('%Y-%m-%d')
        hora_actual = instancia.hora.strftime('%H:%M')

        # Pasar los valores actuales como valores iniciales al formulario
        form = EditarCitaForm(instance=instancia, initial={'fecha': fecha_actual, 'hora': hora_actual})

    return render(request, "Cita/editar_cita.html", {'form': form})

@login_required
def listar_mascotas(request):
    # Vista para listar mascotas con opciones de búsqueda y paginación

    # Obtener el usuario actualmente logeado
    user = request.user

    # Inicializar la variable de consulta para todas las mascotas
    mascotas = Mascota.objects.all()

    # Obtener el valor de búsqueda del parámetro 'cliente' en la URL
    cliente_query = request.GET.get('cliente')

    if user.is_authenticated:
        # Si el usuario está autenticado

        # Si el usuario es un Cliente, filtrar las mascotas por su cuenta
        if hasattr(user, 'cliente'):
            mascotas = mascotas.filter(cliente=user.cliente)
        elif user.empleado and user.empleado.rol in ['Administrador', 'Recepcionista', 'Veterinario']:
            # Si el usuario es un Empleado con los roles mencionados, no aplicar ningún filtro
            pass
        else:
            # Otros usuarios no permitidos, redireccionar o mostrar un mensaje de error según sea necesario
            # Puedes personalizar esto de acuerdo a tus requerimientos
            return HttpResponse("Acceso no autorizado")

        # Si se proporcionó un valor de búsqueda de cliente, filtrar mascotas por cliente
        if cliente_query:
            mascotas = mascotas.filter(cliente__user__username__icontains=cliente_query)

        # Configurar la paginación
        paginator = Paginator(mascotas, 5)  # Mostrar 5 mascotas por página
        page = request.GET.get('page')  # Obtener el número de página de la solicitud GET

        try:
            mascotas = paginator.page(page)
        except PageNotAnInteger:
            mascotas = paginator.page(1)  # Si la página no es un número entero, mostrar la primera página
        except EmptyPage:
            mascotas = paginator.page(paginator.num_pages)  # Si la página está fuera de rango, mostrar la última página

        # Agregar una variable de contexto para indicar si se ha realizado una búsqueda
        has_search_query_cliente = bool(cliente_query)
    else:
        # Si el usuario no está autenticado, puedes redirigirlo a la página de inicio de sesión o mostrar un mensaje de error
        # Puedes personalizar esto según tus necesidades
        return HttpResponse("Acceso no autorizado")

    return render(request, 'Cita/listar_mascotas.html', {
        'mascotas': mascotas,
        'has_search_query_cliente': has_search_query_cliente,
    })

@login_required
def agregar_mascota(request):
    # Vista para agregar una nueva mascota desde un formulario

    # Obtener el usuario actualmente logeado
    user = request.user

    # Verificar si el usuario tiene el rol de administrador o recepcionista
    if user.is_authenticated and (hasattr(user, 'empleado') and user.empleado.rol in ['Administrador', 'Recepcionista']):
        # Si es un empleado con esos roles, permitirle agregar una mascota para cualquier cliente
        if request.method == "POST":
            form = MascotaForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Mascota agregada con éxito.')
                return redirect('listar_mascotas')
        else:
            form = MascotaForm()
    else:
        # Si es un cliente, permitirle agregar una mascota solo para sí mismo
        if request.method == "POST":
            form = MascotaForm(request.POST, user=user)  # Pasa el usuario actual al formulario
            if form.is_valid():
                form.save()
                messages.success(request, 'Mascota agregada con éxito.')
                return redirect('listar_mascotas')
        else:
            form = MascotaForm(user=user)  # Pasa el usuario actual al formulario

    return render(request, "Cita/agregar_mascota.html", {'form': form})

@login_required
def confirmar_borrar_mascota(request, mascota_id):
    # Vista para confirmar la eliminación de una mascota

    mascota = Mascota.objects.get(id=mascota_id)
    return render(request, 'Cita/confirmar_borrar_mascota.html', {'mascota': mascota})

@login_required
def borrar_mascota(request, mascota_id):
    # Vista para borrar una mascota existente

    try:
        instancia = Mascota.objects.get(id=mascota_id)
        instancia.delete()
        messages.success(request, 'Mascota eliminada con éxito.')  # Agrega mensaje de éxito
    except Mascota.DoesNotExist:
        pass  # Manejar la situación en la que la mascota no existe

    return redirect('listar_mascotas')  # Redirige a la lista de mascotas después de borrar

@login_required
def editar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, pk=mascota_id)
    
    if request.method == "POST":
        form = EditarMascotaForm(request.POST, instance=mascota)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mascota editada con éxito.')
            return redirect('listar_mascotas')
    else:
        form = EditarMascotaForm(instance=mascota)
    
    return render(request, 'Cita/editar_mascota.html', {'form': form, 'mascota': mascota})
