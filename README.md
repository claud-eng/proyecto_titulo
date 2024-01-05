README.md para el Repositorio de GitHub del proyecto Sistema de Gestión Centro de Cuidado Huellas Sanas

El proyecto Sistema de Gestión Centro de Cuidado Huellas Sanas, desarrollado por Marcelo y Claudio, ofrece una solución integral para mejorar la experiencia de clientes y empleados de la veterinaria. Incluye una plataforma en línea para gestionar cuentas y registros de mascotas, una tienda online con un sistema de pago seguro, y la gestión de citas. Adicionalmente, cuenta con un sistema de gestión de inventario, administración de personal, generación de informes estadísticos y recursos para 
el cuidado de mascotas. Destaca su sistema POS para el Recepcionista, que optimiza las ventas realizadas de forma presencial y el seguimiento de transacciones. El proyecto busca mejorar la eficiencia del centro y enriquecer la experiencia del cliente.

Estado del Proyecto

El proyecto del Centro de Cuidado Huellas Sanas se encuentra finalizado.

Requisitos del Entorno de Desarrollo

Para integrar y ejecutar el sistema del Centro de Cuidado Huellas Sanas, es necesario contar con:

    Git: https://gitforwindows.org/
    Cuenta en GitHub: https://github.com/
    MySQL: https://dev.mysql.com/downloads/installer/
    Visual Studio Code: https://code.visualstudio.com/download
    Python: https://www.python.org/downloads/

Guía de Instalación y Funcionamiento

    Clonar el Repositorio:
        Abrir CMD en la ruta deseada.
        Ejecutar: git clone https://github.com/claud-eng/proyecto_titulo.git

    Configurar Ambiente Virtual:
        Navegar al directorio clonado: cd proyecto_titulo
        Actualizar pip: pip install --upgrade pip
        Instalar Django: pip install Django
        Navegar al ambiente virtual: cd ambiente_virtual cd Scripts
        Activar el ambiente virtual: activate

    Instalar Dependencias:
        Regresar a la carpeta raíz: cd.. cd..
        Instalar dependencias: pip install -r ambiente.txt

    Configuración de la Base de Datos:
        Abrir MySQL Workbench 8.0 CE y conectarse a una instancia local.
        Ejecutar:

    DROP DATABASE db;
    CREATE DATABASE db CHARACTER SET utf8mb4;
    CREATE USER claud@localhost IDENTIFIED BY 'admin'; 
    GRANT ALL PRIVILEGES ON db.* TO claud@localhost; 
    FLUSH PRIVILEGES;

Migración de la Base de Datos:

    Navegar a cd huellas_sanas.
    Ejecutar:

        python manage.py makemigrations
        python manage.py migrate

    Poblar la Base de Datos:
        Ejecutar el script llamado: Script db.sql ubicado en el siguiente enlace:

        https://drive.google.com/file/d/1nu9E6yCX29mS0j_CfD-XO_ZIpArw8683/view?usp=sharing

        Nota: Al ejecutar el script, se abrirá una ventana, seleccionar la opción Don't Save.

    Configuración Final:
        Abrir settings.py en proyecto_titulo/huellas_sanas/huellas_sanas.
        Configurar EMAIL_HOST_PASSWORD con la API key de SendGrid.
        Obtener el código de la API key en el siguiente link: 

        https://drive.google.com/file/d/14clPNly0CYS4EXgOTMjzyundTrGS0JpB/view?usp=sharing

    Ejecución del Sistema:
        En la consola, en el directorio del manage.py, ejecutar: python manage.py runserver.
        Acceder vía navegador a: http://localhost:8000/.

Cuentas de Prueba

    Correo Gmail de la Empresa:
        Email: huellassanas2023@gmail.com
        Contraseña: duoc@2023

    Cuentas Precargadas en la Base de Datos:
        Cliente: czamorano1995@gmail.com
        Cliente 2: marcela@gmail.com
        Administrador: andrea@huellassanas.cl
        Veterinario: lydia@huellassanas.cl
        Veterinario 2: amanda@huellassanas.cl
        Recepcionista: francisca@huellassanas.cl
        Contraseña para todas: duoc@2023
        
En este link puedes encontrar las tarjetas de prueba para realizar los pagos tras añadir productos y/o servicios al carrito de compras: 

https://www.transbankdevelopers.cl/documentacion/como_empezar#tarjetas-de-prueba
