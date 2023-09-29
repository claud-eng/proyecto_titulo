from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from apps.Usuario.models import Cliente, Empleado  # Importa las clases Cliente y Empleado

# Create your models here.

# Clase para almacenar información sobre las mascotas de los clientes
class Mascota(models.Model):
    ESPECIES_CHOICES = (
        ('Perro', 'Perro'),
        ('Gato', 'Gato'),
    )

    RAZAS_CHOICES = (
        ('Perro', (
            ('Akita Inu', 'Akita Inu'),
            ('Alaskan Malamute', 'Alaskan Malamute'),
            ('Barzoi', 'Barzoi'),
            ('Basset Azul de Gascuña', 'Basset Azul de Gascuña'),
            ('Basset Hound', 'Basset Hound'),
            ('Beagle', 'Beagle'),
            ('Beagle Harrier', 'Beagle Harrier'),
            ('Beauceron', 'Beauceron'),
            ('Bichón Maltés', 'Bichón Maltés'),
            ('Bobtail', 'Bobtail'),
            ('Border Collie', 'Border Collie'),
            ('Boxer', 'Boxer'),
            ('Boyero de Berna', 'Boyero de Berna'),
            ('Braco Alemán', 'Braco Alemán'),
            ('Braco Francés', 'Braco Francés'),
            ('Briard', 'Briard'),
            ('Bull terrier Inglés', 'Bull terrier Inglés'),
            ('Bulldog Francés', 'Bulldog Francés'),
            ('Bulldog Inglés', 'Bulldog Inglés'),
            ('Bullmastiff', 'Bullmastiff'),
            ('Cairn Terrier', 'Cairn Terrier'),
            ('Cane Corso', 'Cane Corso'),
            ('Caniche', 'Caniche'),
            ('Cavalier King Charles', 'Cavalier King Charles'),
            ('Chihuahua', 'Chihuahua'),
            ('Chow Chow', 'Chow Chow'),
            ('Cocker Spaniel Americano', 'Cocker Spaniel Americano'),
            ('Cocker Spaniel Inglés', 'Cocker Spaniel Inglés'),
            ('Collie Rough', 'Collie Rough'),
            ('Collie Smooth', 'Collie Smooth'),
            ('Dálmata', 'Dálmata'),
            ('Doberman', 'Doberman'),
            ('Dogo Argentino', 'Dogo Argentino'),
            ('Dogo de Burdeos', 'Dogo de Burdeos'),
            ('Epagneul Bretón', 'Epagneul Bretón'),
            ('Epagneul Francés', 'Epagneul Francés'),
            ('Epagneul Japonés', 'Epagneul Japonés'),
            ('Fox Terrier', 'Fox Terrier'),
            ('Galgo Español', 'Galgo Español'),
            ('Galgo Irlandés', 'Galgo Irlandés'),
            ('Golden Retriever', 'Golden Retriever'),
            ('Gordon Setter', 'Gordon Setter'),
            ('Gos d\'Atura', 'Gos d\'Atura'),
            ('Gran Danés', 'Gran Danés'),
            ('Husky Siberiano', 'Husky Siberiano'),
            ('Komondor', 'Komondor'),
            ('Labrador Retriever', 'Labrador Retriever'),
            ('Lebrel Afgano', 'Lebrel Afgano'),
            ('Lebrel Polaco', 'Lebrel Polaco'),
            ('Mastiff', 'Mastiff'),
            ('Mastín de los Pirineos', 'Mastín de los Pirineos'),
            ('Mastín Español', 'Mastín Español'),
            ('Mastín Napolitano', 'Mastín Napolitano'),
            ('Montaña de los Pirineos', 'Montaña de los Pirineos'),
            ('Norfolk Terrier', 'Norfolk Terrier'),
            ('Norwich Terrier', 'Norwich Terrier'),
            ('Papillon', 'Papillon'),
            ('Pastor Alemán', 'Pastor Alemán'),
            ('Pastor Australiano', 'Pastor Australiano'),
            ('Pastor Belga', 'Pastor Belga'),
            ('Pastor Blanco Suizo', 'Pastor Blanco Suizo'),
            ('Pastor de los Pirineos', 'Pastor de los Pirineos'),
            ('Pekinés', 'Pekinés'),
            ('Pequeño Azul de Gascuña', 'Pequeño Azul de Gascuña'),
            ('Pequeño Basset Griffon', 'Pequeño Basset Griffon'),
            ('Pequeño Brabantino', 'Pequeño Brabantino'),
            ('Pequeño Perro León', 'Pequeño Perro León'),
            ('Pequeño Perro Ruso', 'Pequeño Perro Ruso'),
            ('Pequeño Sabueso Suizo', 'Pequeño Sabueso Suizo'),
            ('Perdiguero de Burgos', 'Perdiguero de Burgos'),
            ('Perdiguero Portugués', 'Perdiguero Portugués'),
            ('Perro de Agua Español', 'Perro de Agua Español'),
            ('Perro Lobo de Checoslovaquia', 'Perro Lobo de Checoslovaquia'),
            ('Pinscher miniatura', 'Pinscher miniatura'),
            ('Pit Bull', 'Pit Bull'),
            ('Podenco Canario', 'Podenco Canario'),
            ('Podenco Ibicenco', 'Podenco Ibicenco'),
            ('Pointer Inglés', 'Pointer Inglés'),
            ('Presa Canario', 'Presa Canario'),
            ('Pug', 'Pug'),
            ('Rafeiro do Alentejo', 'Rafeiro do Alentejo'),
            ('Rottweiler', 'Rottweiler'),
            ('Samoyedo', 'Samoyedo'),
            ('San Bernardo', 'San Bernardo'),
            ('Schnauzer gigante', 'Schnauzer gigante'),
            ('Schnauzer mediano', 'Schnauzer mediano'),
            ('Schnauzer miniatura', 'Schnauzer miniatura'),
            ('Scottish Terrier', 'Scottish Terrier'),
            ('Setter Inglés', 'Setter Inglés'),
            ('Setter Irlandés', 'Setter Irlandés'),
            ('Shar Pei', 'Shar Pei'),
            ('Shih Tzu', 'Shih Tzu'),
            ('Spitz', 'Spitz'),
            ('Springer Spaniel Galés', 'Springer Spaniel Galés'),
            ('Springer Spaniel Inglés', 'Springer Spaniel Inglés'),
            ('Teckel', 'Teckel'),
            ('Terranova', 'Terranova'),
            ('Weimaraner', 'Weimaraner'),
            ('Westies', 'Westies'),
            ('Whippet', 'Whippet'),
            ('Yorkshire Terrier', 'Yorkshire Terrier'),
        )),
        ('Gato', (
            ('Abisinio', 'Abisinio'),
            ('Angora', 'Angora'),
            ('Azul Ruso', 'Azul Ruso'),
            ('Balinés', 'Balinés'),
            ('Bengal', 'Bengal'),
            ('Bobtail Japonés', 'Bobtail Japonés'),
            ('Bombay', 'Bombay'),
            ('Británico', 'Británico'),
            ('British Shorthair', 'British Shorthair'),
            ('Burmés', 'Burmés'),
            ('Burmilla', 'Burmilla'),
            ('Cartujo (Chartreux)', 'Cartujo (Chartreux)'),
            ('Cornish Rex', 'Cornish Rex'),
            ('Cymric (Man de pelo largo)', 'Cymric (Man de pelo largo)'),
            ('Del Bosque Noruego', 'Del Bosque Noruego'),
            ('Devon rex', 'Devon rex'),
            ('Exóticos', 'Exóticos'),
            ('Fold escocés', 'Fold escocés'),
            ('Foldex', 'Foldex'),
            ('Habana', 'Habana'),
            ('Himalayo', 'Himalayo'),
            ('Javanés', 'Javanés'),
            ('Korat', 'Korat'),
            ('Maine Coon', 'Maine Coon'),
            ('Manx', 'Manx'),
            ('Mau Egipcio', 'Mau Egipcio'),
            ('Munchkin', 'Munchkin'),
            ('Ocicat', 'Ocicat'),
            ('Oriental', 'Oriental'),
            ('Pelicorto Americano', 'Pelicorto Americano'),
            ('Pelicorto Europeo', 'Pelicorto Europeo'),
            ('Persas', 'Persas'),
            ('Ragdoll\'s', 'Ragdoll\'s'),
            ('Rex selkirk', 'Rex selkirk'),
            ('Sagrados de Birmania', 'Sagrados de Birmania'),
            ('Siamés', 'Siamés'),
            ('Siberiano', 'Siberiano'),
            ('Singapur', 'Singapur'),
            ('Snowshoe', 'Snowshoe'),
            ('Somalí', 'Somalí'),
            ('Sphynx', 'Sphynx'),
            ('Tonquinés', 'Tonquinés'),
            ('Van turco', 'Van turco'),
        )),
    )

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=50, choices=ESPECIES_CHOICES)
    raza = models.CharField(max_length=50, choices=RAZAS_CHOICES)

    def __str__(self):
        return self.nombre
    
class Cita(models.Model):
    MOTIVO_CHOICES = (
        ('Consulta Médica General', 'Consulta Médica General'),
        ('Esterilización', 'Esterilización'),
        ('Guardería', 'Guardería'),
        ('Peluquería', 'Peluquería'),
        ('Vacunación', 'Vacunación'),
    )

    ESTADO_CHOICES = (
        ('Programada', 'Programada'),
        ('Cancelada', 'Cancelada'),
        ('Realizada', 'Realizada'),
    )

    fecha = models.DateField()
    hora = models.TimeField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    veterinario = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'Veterinario'}  # Filtra por el rol 'Veterinario'
    )
    motivo = models.CharField(max_length=50, choices=MOTIVO_CHOICES)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='Programada')  # Establece el valor por defecto

    def __str__(self):
        return f'Cita para el cliente {self.cliente.user.username} con {self.veterinario.user.username} el {self.fecha} a las {self.hora}'
