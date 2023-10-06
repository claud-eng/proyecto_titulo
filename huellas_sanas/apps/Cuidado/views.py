from django.shortcuts import render, get_object_or_404, redirect
from .models import Ficha
from .forms import FichaForm
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def listar_fichas(request):
    # Vista para listar fichas con opciones de búsqueda y paginación

    # Obtener todas las fichas
    fichas = Ficha.objects.all()

    # Obtener el valor de búsqueda del parámetro 'mascota' en la URL
    mascota_query = request.GET.get('mascota')

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

    return render(request, 'Cuidado/listar_fichas.html', {
        'fichas': fichas,
        'has_search_query_mascota': has_search_query_mascota,
    })

def agregar_ficha(request):
    # Vista para agregar una nueva ficha desde un formulario

    if request.method == "POST":
        form = FichaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ficha agregada con éxito.')  # Agrega mensaje de éxito
            return redirect('listar_fichas')  # Redirige a la lista de fichas después de agregar una nueva
    else:
        form = FichaForm()
        # Establecer la opción vacía como valor inicial del campo cliente
        form.fields['cliente'].initial = None  # None representa la opción vacía
        
    return render(request, "Cuidado/agregar_ficha.html", {'form': form})

def editar_ficha(request, ficha_id):
    # Vista para editar la información de una ficha existente

    instancia = Ficha.objects.get(id=ficha_id)

    if request.method == "POST":
        form = FichaForm(request.POST, instance=instancia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ficha editada con éxito.')
            return redirect('listar_fichas')
    else:
        # Obtener los valores actuales de fecha y lo convierte a cadenas
        fecha_actual = instancia.fecha.strftime('%Y-%m-%d')
        form = FichaForm(instance=instancia, initial={'fecha': fecha_actual})

    return render(request, "Cuidado/editar_ficha.html", {'form': form})

def confirmar_borrar_ficha(request, ficha_id):
    # Vista para confirmar la eliminación de una ficha

    ficha = Ficha.objects.get(id=ficha_id)
    return render(request, 'Cuidado/confirmar_borrar_ficha.html', {'ficha': ficha})

def borrar_ficha(request, ficha_id):
    # Vista para borrar una ficha existente

    try:
        instancia = Ficha.objects.get(id=ficha_id)
        instancia.delete()
        messages.success(request, 'Ficha eliminada con éxito.')  # Agrega mensaje de éxito
    except Ficha.DoesNotExist:
        pass  # Manejar la situación en la que la ficha no existe

    return redirect('listar_fichas')  # Redirige a la lista de fichas después de borrar una

