from email.headerregistry import ContentTypeHeader
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Servicio, Carrito, OrdenDeCompra, DetalleOrden, OrdenDeVenta, DetalleOrdenVenta
from apps.Usuario.models import Cliente
from .forms import ProductoForm, ServicioForm, OrdenDeVentaForm, DetalleOrdenVentaFormset, DetalleOrdenVentaServicioFormset
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
import locale
from django.contrib.contenttypes.models import ContentType
import requests
from django.shortcuts import redirect
from django.db import transaction
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.http import Http404
from django.db.models import Q
from reportlab.pdfgen import canvas
from django.http import HttpResponse
import os
from django.db.models import Count, Sum
from datetime import datetime, timedelta
from calendar import monthrange
import json
from django.core.serializers.json import DjangoJSONEncoder
import calendar
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

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

    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))

        if cantidad <= 0 or cantidad > producto.cantidad_stock:
            return render(request, 'Transaccion/ver_detalles_producto.html', {
                'producto': producto,
                'error_message': 'Cantidad no válida',
            })

        # Verifica si el producto ya está en el carrito del usuario
        carrito_item = Carrito.objects.filter(cliente=request.user, content_type=ContentType.objects.get_for_model(Producto), object_id=producto.id, carrito=1).first()

        if carrito_item:
            # Si el producto ya está en el carrito, actualiza la cantidad
            carrito_item.cantidad += cantidad
            carrito_item.save()
        else:
            # Si no está en el carrito, crea un nuevo registro
            carrito_item = Carrito(
                cliente=request.user,
                content_type=ContentType.objects.get_for_model(Producto),
                object_id=producto.id,
                cantidad=cantidad,
                carrito=1
            )
            carrito_item.save()
        
        return redirect('carrito')

    return render(request, 'Transaccion/ver_detalles_producto.html', {'producto': producto})

def agregar_al_carrito(request, id, tipo):
    cantidad = int(request.POST.get('cantidad', 1))

    if tipo == 'producto':
        item = get_object_or_404(Producto, id=id)
        content_type = ContentType.objects.get_for_model(Producto)
    elif tipo == 'servicio':
        item = get_object_or_404(Servicio, id=id)
        content_type = ContentType.objects.get_for_model(Servicio)
    else:
        # Manejar error o redirigir a una página de error
        pass

    # Verifica si el producto o servicio ya está en el carrito del usuario
    carrito_item = Carrito.objects.filter(cliente=request.user, content_type=content_type, object_id=id, carrito=1).first()

    if carrito_item:
        if tipo == 'servicio':
            # Si es un servicio y ya está en el carrito, muestra un mensaje de error
            messages.error(request, 'El servicio ya se encuentra en el carrito.')
        else:
            # Si es un producto, actualiza la cantidad
            carrito_item.cantidad += cantidad
            carrito_item.save()
    else:
        # Si no está en el carrito, crea un nuevo registro
        carrito_item = Carrito(
            cliente=request.user,
            content_type=content_type,
            object_id=id,
            cantidad=cantidad,
            carrito=1
        )
        carrito_item.save()

    return redirect('carrito')

def carrito(request):
    carrito_items = Carrito.objects.filter(cliente=request.user, carrito=1)

    total = sum(item.obtener_precio_total() for item in carrito_items)

    # Agregar información adicional a los elementos del carrito para indicar si son servicios o productos
    for item in carrito_items:
        if isinstance(item.item, Servicio):
            item.es_servicio = True
        else:
            item.es_servicio = False

    return render(request, 'Transaccion/carrito.html', {'carrito_items': carrito_items, 'total': total})

def realizar_compra(request):
    # Tu lógica para procesar la compra aquí
    return render(request, 'Transaccion/realizar_compra.html')

def eliminar_del_carrito(request, item_id):
    # Busca el elemento del carrito por su ID y asegúrate de que pertenece al usuario actual
    carrito_item = Carrito.objects.filter(id=item_id, cliente=request.user, carrito=1).first()

    if carrito_item is not None:
        # El elemento existe, elimínalo
        carrito_item.delete()
    else:
        # El elemento no existe, puedes manejar esta situación como desees, por ejemplo, mostrar un mensaje de error o redirigir a una página de error.
        raise Http404("El elemento que intentas eliminar no existe o no te pertenece")

    # Redirige de nuevo a la vista del carrito
    return redirect('carrito')

def vaciar_carrito(request):
    # Busca todos los elementos en el carrito del usuario actual
    carrito_items = Carrito.objects.filter(cliente=request.user, carrito=1)
    
    # Elimina todos los elementos del carrito
    carrito_items.delete()

    # Redirige de nuevo a la vista del carrito
    return redirect('carrito')

def aumentar_cantidad(request, item_id):
    carrito_item = Carrito.objects.filter(id=item_id, cliente=request.user, carrito=1).first()

    if carrito_item:
        carrito_item.cantidad += 1
        carrito_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def disminuir_cantidad(request, item_id):
    carrito_item = Carrito.objects.filter(id=item_id, cliente=request.user, carrito=1).first()

    if carrito_item and carrito_item.cantidad > 1:
        carrito_item.cantidad -= 1
        carrito_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@transaction.atomic
def crear_orden_de_compra(usuario, carrito_items, total):
    """
    Esta función crea una orden de compra en la base de datos y asocia los
    elementos del carrito a dicha orden.

    :param usuario: El usuario que está realizando la compra
    :param carrito_items: Los ítems en el carrito de compras
    :param total: El monto total de la orden
    :return: La instancia de la orden de compra creada
    """
    # Crear la orden de compra
    orden = OrdenDeCompra.objects.create(cliente=usuario, total=total)
    
    # Asociar los elementos del carrito a la orden de compra
    for item in carrito_items:
        detalle_orden_kwargs = {
            'orden_compra': orden,
            'precio': item.item.precio,
            'cantidad': item.cantidad
        }
        if isinstance(item.item, Producto):
            detalle_orden_kwargs['producto'] = item.item
        else:
            detalle_orden_kwargs['servicio'] = item.item
        
        DetalleOrden.objects.create(**detalle_orden_kwargs)
    
    # Luego de crear la orden, marcamos los elementos del carrito como comprados
    carrito_items.update(carrito=0)  # Suponiendo que carrito=0 signifique que los ítems fueron comprados

    return orden

def iniciar_transaccion(request):
    carrito_items = Carrito.objects.filter(cliente=request.user, carrito=1)
    total = sum(item.obtener_precio_total() for item in carrito_items)
    orden = crear_orden_de_compra(request.user, carrito_items, total)  # Crear la orden

    # Datos para la API de Webpay
    data = {
        "buy_order": orden.id,
        "session_id": request.session.session_key,
        "amount": total,
        "return_url": settings.WEBPAY_RETURN_URL
    }

    # Headers para la solicitud a la API de Webpay
    headers = {
        "Tbk-Api-Key-Id": settings.WEBPAY_API_KEY_ID,
        "Tbk-Api-Key-Secret": settings.WEBPAY_API_KEY_SECRET,
        "Content-Type": "application/json"
    }

    # Realizar la solicitud a la API de Webpay
    response = requests.post('https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions', json=data, headers=headers)
    
    if response.status_code == 200:
        token = response.json().get('token')
        url = response.json().get('url')

        # Aquí es donde guardas el token en la base de datos
        orden.token_ws = token
        orden.save()  # No olvides guardar la instancia después de modificarla

        # Agrega registros de depuración
        print("Transacción iniciada con éxito. Token:", token)
        print("URL de redirección:", url)

        return redirect(url + "?token_ws=" + token)
    else:
        # Imprime el error para revisarlo en la consola del servidor
        print("Error al iniciar transacción con Webpay: ", response.status_code, response.text)
        pass

WEBPAY_CONFIRMATION_URL = 'https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions'

def actualizar_estado_orden(token, exitosa):
    orden = None
    # Encuentra la orden por token
    try:
        orden = OrdenDeCompra.objects.get(token_ws=token)
    except OrdenDeCompra.DoesNotExist:
        print(f"Orden no encontrada para el token proporcionado: {token}")
        return None  # O manejar de otra manera la ausencia de la orden

    try:
        if exitosa:
            headers = {
                "Content-Type": "application/json"
                # "Authorization": "Bearer tu_token_de_autenticacion" si es necesario
            }
            
            data = {"token": token}
            response = requests.post(WEBPAY_CONFIRMATION_URL, json=data, headers=headers)
            
            if response.status_code == 200:
                response_data = response.json()
                status = response_data.get('status', 'Estado no encontrado en la respuesta de Webpay')

                # Mapeamos los estados de la transacción a los estados de la orden
                estados = {
                    'INITIALIZED': 'Iniciada',
                    'AUTHORIZED': 'Autorizada',
                    'REVERSED': 'Reversada',
                    'FAILED': 'Fallida',
                    'NULLIFIED': 'Anulada',
                    'PARTIALLY_NULLIFIED': 'Parcialmente Anulada',
                    'CAPTURED': 'Capturada',
                }
                orden.estado = estados.get(status, 'Estado Desconocido')
                orden.token_ws = token  # Actualizamos el token por si acaso
                orden.save()  # Guardamos los cambios en la orden
            else:
                error_message = f"Error al confirmar transacción con Webpay: {response.status_code} {response.text}"
                print(error_message)
                orden.estado = 'fallida'
                orden.save()
        else:
            orden.estado = 'rechazada'
            orden.save()
    except Exception as e:
        print(f"Se ha producido un error al actualizar el estado de la orden: {e}")
        orden.estado = 'Error al actualizar'
        orden.save()

    return orden

def verificar_transaccion(token):
    # Configura los headers necesarios para la solicitud a Webpay
    headers = {
        "Content-Type": "application/json",
        # Añade aquí cualquier otro header que necesites
    }

    # Cuerpo de la solicitud, ajusta los campos según la documentación de Webpay
    data = {
        "token": token
    }

    # Realiza la solicitud a la API de Webpay para verificar el estado de la transacción
    response = requests.post(WEBPAY_CONFIRMATION_URL, json=data, headers=headers)

    if response.status_code == 200:
        # Si la respuesta es exitosa, procesa y devuelve la información de la transacción
        response_data = response.json()
        return {
            'estado': response_data.get('estado'),  # Asegúrate de que estos campos corresponden con la respuesta de Webpay
            'detalle': response_data.get('detalle'),  # Ejemplo de otro campo que podrías necesitar
            # Añade aquí cualquier otro dato que necesites de la respuesta
        }
    else:
        # Mejor manejo de errores con registro detallado
        error_detail = f"No se pudo verificar la transacción con Webpay. Código de estado: {response.status_code}, Respuesta: {response.text}"
        print(error_detail)  # Imprime el mensaje de error en la consola del servidor
        # Podrías querer agregar aquí también un registro en un sistema de logging
        return {
            'estado': 'ERROR',
            'detalle': error_detail
        }
    
def retorno_webpay(request):
    token = request.GET.get('token_ws')

    # Llamada a la API de Webpay para confirmar la transacción
    resultado_transaccion = verificar_transaccion(token)

    if resultado_transaccion['estado'] == 'APROBADA':
        # Actualizar el estado de la orden en la base de datos como exitosa
        orden = actualizar_estado_orden(token, exitosa=True)
        # Agrega registros de depuración
        print("Transacción aprobada. Token:", token)
    elif resultado_transaccion['estado'] == 'RECHAZADA':
        # Actualizar el estado de la orden en la base de datos como no exitosa
        orden = actualizar_estado_orden(token, exitosa=False)
        # Agrega registros de depuración
        print("Transacción rechazada. Token:", token)
    else:
        # Manejar otros posibles estados o errores
        mensaje_error = resultado_transaccion.get('detalle', 'Hubo un problema al procesar tu transacción.')
        orden = actualizar_estado_orden(token, exitosa=False)
        # Agrega registros de depuración
        print("Transacción con estado desconocido. Token:", token)
        print("Mensaje de error:", mensaje_error)

    # Ahora debes verificar si 'orden' es None antes de renderizar la página
    if orden:
        contexto = {'orden': orden, 'resultado': resultado_transaccion['estado']}
    else:
        contexto = {'error': 'Hubo un problema al procesar tu transacción.'}

    # Renderizar la página con los detalles de la transacción
    return render(request, 'Transaccion/retorno_webpay.html', contexto)

@login_required
def agregar_venta(request):
    orden_venta_form = OrdenDeVentaForm(request.POST or None)
    detalle_formset = DetalleOrdenVentaFormset(request.POST or None, prefix='productos')
    detalle_servicio_formset = DetalleOrdenVentaServicioFormset(request.POST or None, prefix='servicios')
    query_string = request.GET.urlencode()

    if request.method == 'POST':
        if orden_venta_form.is_valid() and detalle_formset.is_valid() and detalle_servicio_formset.is_valid():
            # Calculamos el total de productos
            total_productos = sum(form.cleaned_data.get('cantidad', 0) * form.cleaned_data.get('producto').precio for form in detalle_formset if form.cleaned_data.get('producto'))

            # Calculamos el total de servicios
            total_servicios = sum(form.cleaned_data.get('servicio').precio for form in detalle_servicio_formset if form.cleaned_data.get('servicio'))

            # Sumamos ambos totales
            total_venta = total_productos + total_servicios

            # Obtenemos el pago del cliente
            pago_cliente = orden_venta_form.cleaned_data.get('pago_cliente')

            # Comprobamos si el pago del cliente es suficiente
            if pago_cliente < total_venta:
                messages.error(request, 'La cantidad ingresada a pagar es inferior al total de la venta.')
                return render(request, 'Transaccion/agregar_venta.html', {
                    'orden_venta_form': orden_venta_form,
                    'detalle_formset': detalle_formset,
                    'detalle_servicio_formset': detalle_servicio_formset,
                    'query_string': query_string,
                })

            # Aseguramos que el stock es suficiente
            stock_insuficiente = False
            for form in detalle_formset:
                if form.cleaned_data.get('producto'):
                    producto = form.cleaned_data['producto']
                    cantidad = form.cleaned_data['cantidad']
                    if cantidad > producto.cantidad_stock:
                        stock_insuficiente = True
                        messages.error(request, f'Stock insuficiente para el producto {producto.nombre}.')
                        break

            if stock_insuficiente:
                return render(request, 'Transaccion/agregar_venta.html', {
                    'orden_venta_form': orden_venta_form,
                    'detalle_formset': detalle_formset,
                    'detalle_servicio_formset': detalle_servicio_formset,
                    'query_string': query_string,
                })

            with transaction.atomic():
                # Creamos y guardamos la instancia de orden de venta
                orden_venta = orden_venta_form.save(commit=False)
                orden_venta.total = total_venta
                orden_venta.cambio = max(pago_cliente - total_venta, 0)
                orden_venta.save()

                # Actualizamos el stock y guardamos detalles de productos
                for form in detalle_formset:
                    if form.cleaned_data.get('producto'):
                        producto = form.cleaned_data['producto']
                        cantidad = form.cleaned_data['cantidad']
                        producto.cantidad_stock -= cantidad
                        producto.save()

                        detalle = form.save(commit=False)
                        detalle.orden_venta = orden_venta
                        detalle.save()

                # Guardamos detalles de servicios
                for form in detalle_servicio_formset:
                    if form.cleaned_data.get('servicio'):
                        detalle = form.save(commit=False)
                        detalle.orden_venta = orden_venta
                        detalle.save()

                messages.success(request, 'Venta registrada exitosamente.')
                return redirect('listar_ventas')

        else:
            messages.error(request, 'Errores en el formulario de venta')

    context = {
        'orden_venta_form': orden_venta_form,
        'detalle_formset': detalle_formset,
        'detalle_servicio_formset': detalle_servicio_formset,
        'query_string': query_string,
    }
    return render(request, 'Transaccion/agregar_venta.html', context)

@login_required
def listar_ventas(request):
    # Obtener el valor de búsqueda del cliente desde la URL
    cliente_query = request.GET.get('cliente', '')

    # Inicializar una consulta vacía
    query = Q()

    # Si el usuario es un cliente, solo muestra sus ventas
    if hasattr(request.user, 'cliente'):
        query &= Q(cliente=request.user.cliente)
    elif hasattr(request.user, 'empleado') and request.user.empleado.rol == 'Recepcionista':
        if cliente_query:
            query &= Q(cliente__user__username__icontains=cliente_query)
    else:
        # Redireccionar a otra página si el usuario no tiene permiso
        return redirect('home')

    # Filtrar las ventas según la consulta construida
    ventas_filtradas = OrdenDeVenta.objects.filter(query).order_by('id')

    # Configurar la paginación
    paginator = Paginator(ventas_filtradas, 5)  # Mostrar 5 ventas por página
    page = request.GET.get('page')

    try:
        ventas_paginadas = paginator.page(page)
    except PageNotAnInteger:
        ventas_paginadas = paginator.page(1)
    except EmptyPage:
        ventas_paginadas = paginator.page(paginator.num_pages)

    ventas_list = []
    for venta in ventas_paginadas:
        productos = venta.detalleordenventa_set.filter(producto__isnull=False)
        servicios = venta.detalleordenventa_set.filter(servicio__isnull=False)
        # Agregar la información de productos y servicios al contexto de la plantilla
        ventas_list.append({
            'venta': venta,
            'productos': productos,
            'servicios': servicios,
            'tiene_productos': productos.exists(),
            'tiene_servicios': servicios.exists(),
        })

    return render(request, 'Transaccion/listar_ventas.html', {
        'ventas_list': ventas_list,
        'ventas_paginadas': ventas_paginadas,
        'cliente_query': cliente_query,  # Agregamos esta línea para utilizarla en la plantilla HTML
    })

logo_path = os.path.join(settings.BASE_DIR, 'apps/static/images/img/logo.png')

@login_required
def generar_comprobante(request, id_venta):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="comprobante_venta_{id_venta}.pdf"'

    p = canvas.Canvas(response)
    venta = OrdenDeVenta.objects.get(id=id_venta)
    detalles = venta.detalleordenventa_set.all()

    y = 800  # Posición inicial en el eje Y para el texto

    # Añadir el nombre de la empresa
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, y, "Empresa: Huellas Sanas S.A.")
    y -= 20  # Ajustar el eje Y para el siguiente texto

    # Detalles de la venta
    p.drawString(100, y, f"Orden de Venta: {venta.id}")

    # Verificar si el correo electrónico del cliente es diferente de anonimo@gmail.com
    if venta.cliente.user.username != "anonimo@gmail.com":
        p.drawString(100, y-20, f"Cliente: {venta.cliente.user.username}")
        y -= 40  # Ajustar el eje Y para el siguiente texto (con nombre del cliente)
    else:
        y -= 20  # Ajustar menos el eje Y si se omite el nombre del cliente

    p.drawString(100, y-20, f"Fecha: {venta.fecha_creacion.strftime('%d/%m/%Y %H:%M')}")
    p.drawString(100, y-40, "Detalle:")

    # Detalles de productos y servicios
    y -= 80
    for detalle in detalles:
        if detalle.producto:
            p.drawString(120, y, f"Producto: {detalle.producto.nombre} - Cantidad: {detalle.cantidad} - Precio Unitario: ${detalle.producto.precio}")
            y -= 20
        if detalle.servicio:
            p.drawString(120, y, f"Servicio: {detalle.servicio.nombre} - Precio: ${detalle.servicio.precio}")
            y -= 20

    p.drawString(100, y-20, f"Total: ${venta.total}")
    p.drawString(100, y-40, f"Pagó: ${venta.pago_cliente}")
    p.drawString(100, y-60, f"Vuelto: ${venta.cambio}")

    p.showPage()
    p.save()
    return response

@login_required
def gestionar_compras(request):
    # Aquí puedes agregar la lógica para gestionar cuentas de usuarios
    return render(request, 'Transaccion/gestionar_compras.html')

def top_cinco_productos_vendidos(anio, mes):
    fecha_inicio = datetime(anio, mes, 1)
    fecha_fin = datetime(anio, mes + 1, 1) if mes < 12 else datetime(anio + 1, 1, 1)
    return Producto.objects.filter(detalleordenventa__orden_venta__fecha_creacion__range=[fecha_inicio, fecha_fin]).annotate(total_vendido=Sum('detalleordenventa__cantidad')).order_by('-total_vendido')[:5]

def top_cinco_servicios_vendidos(anio, mes):
    fecha_inicio = datetime(anio, mes, 1)
    fecha_fin = datetime(anio, mes + 1, 1) if mes < 12 else datetime(anio + 1, 1, 1)
    return Servicio.objects.filter(detalleordenventa__orden_venta__fecha_creacion__range=[fecha_inicio, fecha_fin]).annotate(total_vendido=Sum('detalleordenventa__cantidad')).order_by('-total_vendido')[:5]

def generar_grafico_base64(datos):
    fig, ax = plt.subplots()
    ax.pie(datos['values'], labels=datos['labels'], autopct='%1.1f%%')
    plt.axis('equal')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    return graphic

def reportes_ventas(request):
    anio_actual = datetime.now().year
    mes_actual = datetime.now().month

    anio = int(request.GET.get('anio', anio_actual))
    mes = int(request.GET.get('mes', mes_actual))

    top_cinco_productos = top_cinco_productos_vendidos(anio, mes)
    top_cinco_servicios = top_cinco_servicios_vendidos(anio, mes)

    mensaje_productos = ""
    mensaje_servicios = ""

    if not top_cinco_productos:
        mensaje_productos = "No se han registrado ventas de productos en el mes seleccionado."

    if not top_cinco_servicios:
        mensaje_servicios = "No se han registrado ventas de servicios en el mes seleccionado."

    datos_productos = json.dumps({
        'labels': [producto.nombre for producto in top_cinco_productos],
        'data': [producto.total_vendido for producto in top_cinco_productos]
    }, cls=DjangoJSONEncoder) if top_cinco_productos else json.dumps({})

    datos_servicios = json.dumps({
        'labels': [servicio.nombre for servicio in top_cinco_servicios],
        'data': [servicio.total_vendido for servicio in top_cinco_servicios]
    }, cls=DjangoJSONEncoder) if top_cinco_servicios else json.dumps({})

    # Diccionario de nombres de meses en español
    meses = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
        5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
        9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }

    nombre_mes = meses.get(mes, "Mes desconocido")

    datos_grafico = {
        'labels': [producto.nombre for producto in top_cinco_productos],
        'values': [producto.total_vendido for producto in top_cinco_productos]
    }
    imagen_grafico = generar_grafico_base64(datos_grafico)

    contexto = {
        'datos_productos_json': datos_productos,
        'datos_servicios_json': datos_servicios,
        'mensaje_productos': mensaje_productos,
        'mensaje_servicios': mensaje_servicios,
        'rango_anios': range(2022, 2028),
        'rango_meses': range(1, 13),
        'anio_actual': anio_actual,
        'mes_actual': mes_actual,
        'anio_seleccionado': anio,
        'mes_seleccionado': mes,
        'nombre_mes': nombre_mes,
        'imagen_grafico': imagen_grafico,
        'top_cinco_productos': top_cinco_productos,
        'top_cinco_servicios': top_cinco_servicios,
    }

    return render(request, 'Transaccion/reportes_ventas.html', contexto)

MES_ESPANOL = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
    5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
    9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
}

def exportar_pdf(request):
    anio = request.GET.get('anioParaPDF', str(datetime.now().year))
    mes = request.GET.get('mesParaPDF', str(datetime.now().month))

    top_cinco_productos = top_cinco_productos_vendidos(int(anio), int(mes))
    top_cinco_servicios = top_cinco_servicios_vendidos(int(anio), int(mes))
    # Calcular el total vendido de productos y servicios
    total_vendido_productos = sum([producto.total_vendido for producto in top_cinco_productos])
    total_vendido_servicios = sum([servicio.total_vendido for servicio in top_cinco_servicios])
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_ventas_{anio}_{mes}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    nombre_mes = MES_ESPANOL.get(int(mes), "Mes desconocido")

    # La posición inicial en la página
    y_position = 750

    # Títulos de los gráficos
    p.drawString(100, y_position, f"Reporte de Ventas del mes {nombre_mes} del año {anio}")
    y_position -= 40

    # Dibujo del gráfico de productos
    if top_cinco_productos:
        p.drawString(100, y_position, "Top 5 Productos Más Vendidos")
        y_position -= 20

        datos_para_grafico_productos = {
            'labels': [producto.nombre for producto in top_cinco_productos],
            'values': [producto.total_vendido for producto in top_cinco_productos]
        }
        imagen_grafico_productos = generar_grafico_base64(datos_para_grafico_productos)
        imagen_grafico_productos = ImageReader(BytesIO(base64.b64decode(imagen_grafico_productos)))
        p.drawImage(imagen_grafico_productos, 100, y_position - 220, width=400, height=200)

        y_position -= 220 + 20

        data_productos = [['Producto', 'Cantidad', 'Porcentaje']]
        for producto in top_cinco_productos:
            porcentaje = (producto.total_vendido / total_vendido_productos * 100) if total_vendido_productos else 0
            data_productos.append([producto.nombre, producto.total_vendido, f"{porcentaje:.2f}%"])
        tabla_productos = Table(data_productos, colWidths=[200, 100, 100], hAlign='LEFT')
        tabla_productos.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        tabla_productos.wrapOn(p, 400, 200)
        tabla_productos.drawOn(p, 100, y_position - 20 * len(data_productos) - 10)
        y_position -= 20 * len(data_productos) + 30

    else:
        # Después de dibujar el título "Top 5 Productos Más Vendidos"
        p.drawString(100, y_position, "Top 5 Productos Más Vendidos")
        y_position -= 40  # Tres líneas de espacio, asumiendo aproximadamente 20 puntos por línea

        # Ahora dibujamos el mensaje de "No se han registrado ventas..."
        p.drawString(100, y_position, "No se han registrado ventas de productos en el mes seleccionado.")
        y_position -= 30  # Ajustamos para la próxima línea o sección

    # Inmediatamente creamos una nueva página para los servicios
    p.showPage()
    y_position = 750
    p.drawString(100, y_position, "Top 5 Servicios Más Vendidos")
    y_position -= 40

    # Dibujo del gráfico de servicios en la segunda página
    if top_cinco_servicios:
        datos_para_grafico_servicios = {
            'labels': [servicio.nombre for servicio in top_cinco_servicios],
            'values': [servicio.total_vendido for servicio in top_cinco_servicios]
        }
        imagen_grafico_servicios = generar_grafico_base64(datos_para_grafico_servicios)
        imagen_grafico_servicios = ImageReader(BytesIO(base64.b64decode(imagen_grafico_servicios)))
        p.drawImage(imagen_grafico_servicios, 100, y_position - 220, width=400, height=200)
        y_position -= 220 + 20

        data_servicios = [['Servicio', 'Cantidad', 'Porcentaje']]
        for servicio in top_cinco_servicios:
            porcentaje = (servicio.total_vendido / total_vendido_servicios * 100) if total_vendido_servicios else 0
            data_servicios.append([servicio.nombre, servicio.total_vendido, f"{porcentaje:.2f}%"])
        tabla_servicios = Table(data_servicios, colWidths=[200, 100, 100], hAlign='LEFT')
        tabla_servicios.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        tabla_servicios.wrapOn(p, 400, 200)
        tabla_servicios.drawOn(p, 100, y_position - 20 * len(data_servicios) - 10)
        y_position -= 20 * len(data_servicios) + 30

    else:
        p.drawString(100, y_position, "No se han registrado ventas de servicios en el mes seleccionado.")
        y_position -= 30

    # Guardar el PDF en el objeto de respuesta
    p.save()
    return response