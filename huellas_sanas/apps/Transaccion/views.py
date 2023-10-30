from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Servicio
from .forms import ProductoForm, ServicioForm
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
import locale

@login_required
def listar_productos(request):
    from django.db.models import Q

    # Obtener todos los productos
    productos = Producto.objects.all()

    # Obtener los valores de los filtros desde la URL
    nombre_query = request.GET.get('nombre')
    stock_query = request.GET.get('stock')
    categoria_filter = request.GET.get('categoria')
    marca_query = request.GET.get('marca')
    sort_order = request.GET.get('sort')

    # Inicializar una consulta vacía
    query = Q()

    # Aplicar los filtros según las selecciones del usuario
    if nombre_query:
        query &= Q(nombre__icontains=nombre_query)

    if categoria_filter:
        query &= Q(categoria=categoria_filter)

    if marca_query:
        query &= Q(marca__icontains=marca_query)

    # Construir una lista de órdenes de ordenamiento para aplicar al final
    sort_orders = []

    if sort_order == 'asc':
        sort_orders.append('precio')
    elif sort_order == 'desc':
        sort_orders.append('-precio')

    if stock_query == 'asc':
        sort_orders.append('cantidad_stock')
    elif stock_query == 'desc':
        sort_orders.append('-cantidad_stock')

    # Aplicar los filtros y ordenamiento en un solo paso
    productos = productos.filter(query).order_by(*sort_orders)

    # Configurar la paginación
    paginator = Paginator(productos, 5)
    page = request.GET.get('page')

    try:
        productos = paginator.page(page)
    except PageNotAnInteger:
        productos = paginator.page(1)
    except EmptyPage:
        productos = paginator.page(paginator.num_pages)

    # Agregar una variable de contexto para indicar si se ha realizado una búsqueda
    has_search_query_nombre = bool(nombre_query)

    return render(request, 'Transaccion/listar_productos.html', {
        'productos': productos,
        'has_search_query_nombre': has_search_query_nombre,
    })

@login_required
def agregar_producto(request):
    # Vista para agregar un nuevo producto desde un formulario

    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)  # Asegúrate de incluir request.FILES para manejar la imagen
        if form.is_valid():
            producto = form.save(commit=False)  # Guarda el formulario sin guardar en la base de datos
            producto.imagen = form.cleaned_data['imagen']  # Asigna la imagen del formulario al producto
            producto.save()  # Guarda el producto en la base de datos
            messages.success(request, 'Producto agregado con éxito.')  # Agrega mensaje de éxito
            return redirect('listar_productos')  # Redirige a la lista de productos después de agregar uno nuevo
    else:
        form = ProductoForm()
    return render(request, "Transaccion/agregar_producto.html", {'form': form})

@login_required
def editar_producto(request, producto_id):
    # Vista para editar la información de un producto existente

    instancia = Producto.objects.get(id=producto_id)

    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=instancia)
        if form.is_valid():
            producto = form.save(commit=False)  # Guarda el formulario sin guardar en la base de datos
            if 'imagen' in request.FILES:
                producto.imagen = form.cleaned_data['imagen']  # Asigna la nueva imagen del formulario al producto
            producto.save()  # Guarda el producto en la base de datos

            messages.success(request, 'Producto editado con éxito.')
            return redirect('listar_productos')
    else:
        form = ProductoForm(instance=instancia)

    return render(request, "Transaccion/editar_producto.html", {'form': form})

@login_required
def confirmar_borrar_producto(request, producto_id):
    # Vista para confirmar la eliminación de un producto

    producto = Producto.objects.get(id=producto_id)
    return render(request, 'Transaccion/confirmar_borrar_producto.html', {'producto': producto})

@login_required
def borrar_producto(request, producto_id):
    # Vista para borrar un producto existente

    try:
        instancia = Producto.objects.get(id=producto_id)
        instancia.delete()
        messages.success(request, 'Producto eliminado con éxito.')  # Agrega mensaje de éxito
    except Producto.DoesNotExist:
        pass  # Manejar la situación en la que el producto no existe

    return redirect('listar_productos')  # Redirige a la lista de productos después de borrar uno

@login_required
def listar_servicios(request):
    # Vista para listar servicios con opciones de búsqueda y paginación

    # Obtener todos los servicios
    servicios = Servicio.objects.all()

    # Obtener el valor de búsqueda del parámetro 'nombre' en la URL
    nombre_query = request.GET.get('nombre')

    # Si se proporcionó un valor de búsqueda de nombre, filtrar servicios por nombre
    if nombre_query:
        servicios = servicios.filter(nombre__icontains=nombre_query)

    # Configurar la paginación
    paginator = Paginator(servicios, 5)  # Mostrar 5 servicios por página
    page = request.GET.get('page')  # Obtener el número de página de la solicitud GET

    try:
        servicios = paginator.page(page)
    except PageNotAnInteger:
        servicios = paginator.page(1)  # Si la página no es un número entero, mostrar la primera página
    except EmptyPage:
        servicios = paginator.page(paginator.num_pages)  # Si la página está fuera de rango, mostrar la última página

    # Agregar una variable de contexto para indicar si se ha realizado una búsqueda
    has_search_query_nombre = bool(nombre_query)

    return render(request, 'Transaccion/listar_servicios.html', {
        'servicios': servicios,
        'has_search_query_nombre': has_search_query_nombre,
    })

@login_required
def agregar_servicio(request):
    # Vista para agregar un nuevo servicio desde un formulario

    if request.method == "POST":
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Servicio agregado con éxito.')  # Agrega mensaje de éxito
            return redirect('listar_servicios')  # Redirige a la lista de servicios después de agregar uno nuevo
    else:
        form = ServicioForm()
    return render(request, "Transaccion/agregar_servicio.html", {'form': form})

@login_required
def editar_servicio(request, servicio_id):
    # Vista para editar la información de un servicio existente

    instancia = Servicio.objects.get(id=servicio_id)

    if request.method == "POST":
        form = ServicioForm(request.POST, instance=instancia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Servicio editado con éxito.')
            return redirect('listar_servicios')
    else:
        form = ServicioForm(instance=instancia)

    return render(request, "Transaccion/editar_servicio.html", {'form': form})

@login_required
def confirmar_borrar_servicio(request, servicio_id):
    # Vista para confirmar la eliminación de un servicio

    servicio = Servicio.objects.get(id=servicio_id)
    return render(request, 'Transaccion/confirmar_borrar_servicio.html', {'servicio': servicio})

@login_required
def borrar_servicio(request, servicio_id):
    # Vista para borrar un servicio existente

    try:
        instancia = Servicio.objects.get(id=servicio_id)
        instancia.delete()
        messages.success(request, 'Servicio eliminado con éxito.')  # Agrega mensaje de éxito
    except Servicio.DoesNotExist:
        pass  # Manejar la situación en la que el servicio no existe

    return redirect('listar_servicios')  # Redirige a la lista de servicios después de borrar uno

@login_required
def gestionar_inventario(request):
    # Aquí puedes agregar la lógica para gestionar el inventario
    return render(request, 'Transaccion/gestionar_inventario.html')

def catalogo_productos(request):
    # Recupera la selección de orden del parámetro 'sort' en la URL
    sort_order = request.GET.get('sort', '')
    categoria_filter = request.GET.get('categoria', '')

    # Recupera todos los productos desde la base de datos
    productos = Producto.objects.all()

    # Aplica el filtro por categoría
    if categoria_filter:
        productos = productos.filter(categoria=categoria_filter)

    # Ordena los productos según la selección del usuario
    if sort_order == 'asc':
        productos = productos.order_by('precio')
    elif sort_order == 'desc':
        productos = productos.order_by('-precio')

    # Configura la paginación (muestra 10 productos por página)
    paginator = Paginator(productos, 10)
    page = request.GET.get('page')

    try:
        productos = paginator.page(page)
    except PageNotAnInteger:
        productos = paginator.page(1)
    except EmptyPage:
        productos = paginator.page(paginator.num_pages)

    # Formatea los precios de los productos
    for producto in productos:
        producto.precio = locale.format_string('%.0f', producto.precio, grouping=True)

    # Pasa los productos formateados y paginados a la plantilla
    return render(request, 'Transaccion/catalogo_productos.html', {'productos': productos})

def catalogo_servicios(request):
    # Recupera todos los servicios desde la base de datos
    servicios = Servicio.objects.all()
    
    # Configura la ubicación para usar comas como separadores de miles
    locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')

    # Formatea los precios de los servicios
    for servicio in servicios:
        servicio.precio = locale.format_string('%.0f', servicio.precio, grouping=True)

    # Pasa los servicios formateados a la plantilla
    return render(request, 'Transaccion/catalogo_servicios.html', {'servicios': servicios})

def ver_detalles_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'Transaccion/ver_detalles_producto.html', {'producto': producto})