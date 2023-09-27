from django.shortcuts import redirect, render  # Importa funciones para redirigir y renderizar plantillas HTML
from apps.Usuario.models import Cliente, Empleado  # Importa los modelos Cliente y Empleado de la aplicación Usuario
from .forms import ClienteForm, EmpleadoForm, EditarClienteForm, EditarEmpleadoForm  # Importa los formularios definidos en este directorio
from django.contrib import messages  # Importa la clase para trabajar con mensajes de Django
from django.contrib.auth.hashers import make_password  # Importa la función para crear contraseñas seguras
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage  # Importa clases y funciones para paginación

# Create your views here.

def listar_clientes(request):
    # Vista para listar clientes con opciones de búsqueda y paginación

    # Obtener todos los clientes
    clientes = Cliente.objects.all()

    # Obtener los valores de búsqueda de los parámetros 'username' y 'rut' en la URL
    username_query = request.GET.get('username')
    rut_query = request.GET.get('rut')

    # Si se proporcionó un valor de búsqueda de nombre de usuario, filtrar clientes por nombre de usuario
    if username_query:
        clientes = clientes.filter(user__username__icontains=username_query)

    # Si se proporcionó un valor de búsqueda de RUT, filtrar clientes por RUT
    if rut_query:
        clientes = clientes.filter(rut__icontains=rut_query)

    # Configurar la paginación
    paginator = Paginator(clientes, 5)  # Mostrar 5 clientes por página
    page = request.GET.get('page')  # Obtener el número de página de la solicitud GET

    try:
        clientes = paginator.page(page)
    except PageNotAnInteger:
        clientes = paginator.page(1)  # Si la página no es un número entero, mostrar la primera página
    except EmptyPage:
        clientes = paginator.page(paginator.num_pages)  # Si la página está fuera de rango, mostrar la última página

    # Agregar variables de contexto para indicar si se ha realizado una búsqueda
    has_search_query_username = bool(username_query)
    has_search_query_rut = bool(rut_query)

    return render(request, 'Usuario/listar_clientes.html', {
        'clientes': clientes,
        'has_search_query_username': has_search_query_username,
        'has_search_query_rut': has_search_query_rut,
    })

def agregar_cliente(request):
    # Vista para agregar un nuevo cliente desde un formulario

    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente agregado con éxito.')  # Agrega mensaje de éxito
            return redirect('listar_clientes')  # Redirige a la lista de clientes después de agregar uno nuevo
    else:
        form = ClienteForm()
    return render(request, "Usuario/agregar_cliente.html", {'form': form})

def confirmar_borrar_cliente(request, cliente_id):
    # Vista para confirmar la eliminación de un cliente

    cliente = Cliente.objects.get(id=cliente_id)
    return render(request, 'Usuario/confirmar_borrar_cliente.html', {'cliente': cliente})

def borrar_cliente(request, cliente_id):
    # Vista para borrar un cliente existente

    try:
        instancia = Cliente.objects.get(id=cliente_id)
        instancia.delete()
        messages.success(request, 'Cliente eliminado con éxito.')  # Agrega mensaje de éxito
    except Cliente.DoesNotExist:
        pass  # Manejar la situación en la que el cliente no existe

    return redirect('listar_clientes')  # Redirige a la lista de clientes después de borrar

def editar_cliente(request, cliente_id):
    # Vista para editar la información de un cliente existente

    instancia = Cliente.objects.get(id=cliente_id)

    if request.method == "POST":
        form = EditarClienteForm(request.POST, instance=instancia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente editado con éxito.')  # Agrega mensaje de éxito
            return redirect('listar_clientes')  # Redirige a la lista de clientes después de editar
    else:
        form = EditarClienteForm(initial={
            'username': instancia.user.username,
            'first_name': instancia.user.first_name,
            'last_name': instancia.user.last_name,
            'rut': instancia.rut,
            'second_last_name': instancia.second_last_name,
            'fecha_nacimiento': instancia.fecha_nacimiento,
            'numero_telefono': instancia.numero_telefono,
        })
    return render(request, "Usuario/editar_cliente.html", {'form': form})

def listar_empleados(request):
    # Vista para listar empleados con opciones de búsqueda y paginación

    # Obtener todos los empleados
    empleados = Empleado.objects.all()

    # Obtener los valores de búsqueda de los parámetros 'username' y 'rut' en la URL
    username_query = request.GET.get('username')
    rut_query = request.GET.get('rut')

    # Si se proporcionó un valor de búsqueda de nombre de usuario, filtrar empleados por nombre de usuario
    if username_query:
        empleados = empleados.filter(user__username__icontains=username_query)

    # Si se proporcionó un valor de búsqueda de RUT, filtrar empleados por RUT
    if rut_query:
        empleados = empleados.filter(rut__icontains=rut_query)

    # Configurar la paginación
    paginator = Paginator(empleados, 5)  # Mostrar 5 empleados por página
    page = request.GET.get('page')  # Obtener el número de página de la solicitud GET

    try:
        empleados = paginator.page(page)
    except PageNotAnInteger:
        empleados = paginator.page(1)  # Si la página no es un número entero, mostrar la primera página
    except EmptyPage:
        empleados = paginator.page(paginator.num_pages)  # Si la página está fuera de rango, mostrar la última página

    # Agregar variables de contexto para indicar si se ha realizado una búsqueda
    has_search_query_username = bool(username_query)
    has_search_query_rut = bool(rut_query)

    return render(request, 'Usuario/listar_empleados.html', {
        'empleados': empleados,
        'has_search_query_username': has_search_query_username,
        'has_search_query_rut': has_search_query_rut,
    })

def agregar_empleado(request):
    # Vista para agregar un nuevo empleado desde un formulario

    if request.method == "POST":
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado agregado con éxito.')  # Agrega mensaje de éxito
            return redirect('listar_empleados')  # Redirige a la lista de empleados después de agregar uno nuevo
    else:
        form = EmpleadoForm()
    return render(request, "Usuario/agregar_empleado.html", {'form': form})

def confirmar_borrar_empleado(request, empleado_id):
    # Vista para confirmar la eliminación de un empleado

    empleado = Empleado.objects.get(id=empleado_id)
    return render(request, 'Usuario/confirmar_borrar_empleado.html', {'empleado': empleado})

def borrar_empleado(request, empleado_id):
    # Vista para borrar un empleado existente

    try:
        instancia = Empleado.objects.get(id=empleado_id)
        instancia.delete()
        messages.success(request, 'Empleado eliminado con éxito.')  # Agrega mensaje de éxito
    except Empleado.DoesNotExist:
        pass  # Manejar la situación en la que el empleado no existe

    return redirect('listar_empleados')  # Redirige a la lista de empleados después de borrar

def editar_empleado(request, empleado_id):
    # Vista para editar la información de un empleado existente

    instancia = Empleado.objects.get(id=empleado_id)

    if request.method == "POST":
        form = EditarEmpleadoForm(request.POST, instance=instancia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado editado con éxito.')  # Agrega mensaje de éxito
            return redirect('listar_empleados')  # Redirige a la lista de empleados después de editar
    else:
        form = EditarEmpleadoForm(initial={
            'username': instancia.user.username,
            'first_name': instancia.user.first_name,
            'last_name': instancia.user.last_name,
            'rol': instancia.rol,
            'rut': instancia.rut,
            'second_last_name': instancia.second_last_name,
            'fecha_nacimiento': instancia.fecha_nacimiento,
            'numero_telefono': instancia.numero_telefono,
        })
    return render(request, "Usuario/editar_empleado.html", {'form': form})


