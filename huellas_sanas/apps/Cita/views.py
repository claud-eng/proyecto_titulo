from django.shortcuts import render, get_object_or_404, redirect
from .models import Cita, Mascota
from apps.Cita.models import Cita, Mascota
from .forms import CitaForm, EditarCitaForm, MascotaForm, EditarMascotaForm
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def listar_citas(request):
    # Vista para listar citas con opciones de búsqueda y paginación

    # Obtener todas las citas
    citas = Cita.objects.all()

    # Obtener los valores de búsqueda de los parámetros 'cliente' y 'veterinario' en la URL
    cliente_query = request.GET.get('cliente')
    veterinario_query = request.GET.get('veterinario')

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

    return render(request, 'Cita/listar_citas.html', {
        'citas': citas,
        'has_search_query_cliente': has_search_query_cliente,
        'has_search_query_veterinario': has_search_query_veterinario,
    })

def agendar_cita(request):
    # Vista para agregar una nueva cita desde un formulario

    if request.method == "POST":
        form = CitaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cita agregada con éxito.')  # Agrega mensaje de éxito
            return redirect('listar_citas')  # Redirige a la lista de citas después de agregar una nueva
    else:
        form = CitaForm()
    return render(request, "Cita/agendar_cita.html", {'form': form})

def confirmar_borrar_cita(request, cita_id):
    # Vista para confirmar la eliminación de una cita

    cita = Cita.objects.get(id=cita_id)
    return render(request, 'Cita/confirmar_borrar_cita.html', {'cita': cita})

def borrar_cita(request, cita_id):
    # Vista para borrar una cita existente

    try:
        instancia = Cita.objects.get(id=cita_id)
        instancia.delete()
        messages.success(request, 'Cita eliminada con éxito.')  # Agrega mensaje de éxito
    except Cita.DoesNotExist:
        pass  # Manejar la situación en la que la cita no existe

    return redirect('listar_citas')  # Redirige a la lista de citas después de borrar

def editar_cita(request, cita_id):
    # Vista para editar la información de una cita existente

    instancia = Cita.objects.get(id=cita_id)

    if request.method == "POST":
        form = EditarCitaForm(request.POST, instance=instancia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cita editada con éxito.')  # Agrega mensaje de éxito
            return redirect('listar_citas')  # Redirige a la lista de citas después de editar
    else:
        form = EditarCitaForm(instance=instancia)
    return render(request, "Cita/editar_cita.html", {'form': form})

def gestionar_citas(request):
    # Aquí puedes agregar la lógica para gestionar las citas de los usuarios
    return render(request, 'Cita/gestionar_citas.html')

def listar_mascotas(request):
    # Vista para listar mascotas con opciones de búsqueda y paginación

    # Obtener todas las mascotas
    mascotas = Mascota.objects.all()

    # Obtener el valor de búsqueda del parámetro 'cliente' en la URL
    cliente_query = request.GET.get('cliente')

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

    return render(request, 'Cita/listar_mascotas.html', {
        'mascotas': mascotas,
        'has_search_query_cliente': has_search_query_cliente,
    })

def agregar_mascota(request):
    # Vista para agregar una nueva mascota desde un formulario

    if request.method == "POST":
        form = MascotaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mascota agregada con éxito.')  # Agrega mensaje de éxito
            return redirect('listar_mascotas')  # Redirige a la lista de mascotas después de agregar una nueva
    else:
        form = MascotaForm()
    return render(request, "Cita/agregar_mascota.html", {'form': form})

def confirmar_borrar_mascota(request, mascota_id):
    # Vista para confirmar la eliminación de una mascota

    mascota = Mascota.objects.get(id=mascota_id)
    return render(request, 'Cita/confirmar_borrar_mascota.html', {'mascota': mascota})

def borrar_mascota(request, mascota_id):
    # Vista para borrar una mascota existente

    try:
        instancia = Mascota.objects.get(id=mascota_id)
        instancia.delete()
        messages.success(request, 'Mascota eliminada con éxito.')  # Agrega mensaje de éxito
    except Mascota.DoesNotExist:
        pass  # Manejar la situación en la que la mascota no existe

    return redirect('listar_mascotas')  # Redirige a la lista de mascotas después de borrar

def editar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, pk=mascota_id)
    
    if request.method == "POST":
        form = EditarMascotaForm(request.POST, instance=mascota)
        if form.is_valid():
            form.save()
            return redirect('gestionar_mascotas')
    else:
        form = EditarMascotaForm(instance=mascota)
    
    return render(request, 'Cita/editar_mascota.html', {'form': form, 'mascota': mascota})

def gestionar_mascotas(request):
    mascotas = Mascota.objects.all()
    return render(request, "Cita/gestionar_mascotas.html", {'mascotas': mascotas})