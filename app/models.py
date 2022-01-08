from django.db import models
from django.db.models.fields.files import ImageField
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Users(models.Model):
    nombre=models.CharField(max_length=144)
    apellido=models.CharField(max_length=144)
    correo=models.EmailField(max_length=255)
    password=models.CharField(max_length=150)
    isActive=models.BooleanField(null=True, blank=True)
    # image=models.ImageField(upload_to="usuarios", null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"id: {self.id}, Name:{self.nombre}, email:{self.correo}"
class Products(models.Model):
    nombre=models.CharField(max_length=144)
    description=models.TextField()
    precio=models.FloatField()
    image=models.ImageField(upload_to="productos", null=True)
    stock=models.IntegerField(validators=[MinValueValidator(0)])
    category_slug=models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"id: {self.id}, Name:{self.nombre}, category:{self.category_slug}, precio:{self.precio}, image:{self.image}"
class Newsletter_users(models.Model):
    correo=models.EmailField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Categorias(models.Model):
    # Establecemos los valores para el modelo
    INFANTILES='INF'
    FAMILIARES='FAM'
    NAIPES='NAP'
    TODOS='TOD'
    # El segundo parámetro de la tupla es el nombre que los usuarios verán 
    NAMES_CHOICES=[
        (INFANTILES,'Infantiles'),
        (FAMILIARES,'Familiares'),
        (NAIPES,'Naipes'),
        (TODOS,'Todos los Juegos'),
    ]
    # Ropa para niños, para adultos, tecnologías
    name_category=models.CharField(
        max_length=4,
        choices= NAMES_CHOICES,
        default=TODOS,
    )
    key_catogory_list=models.ManyToManyField(Products)

class Profile(models.Model):
    user=models.OneToOneField(Users, on_delete=models.CASCADE, related_name='profile',primary_key=True)
    image = models.ImageField(default='../media/default.jpg', upload_to='usuarios')

    def __str__(self):
        return f'{self.user.nombre} Profile'