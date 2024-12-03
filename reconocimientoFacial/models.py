from django.db import models

# Create your models here.
class Persona(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    imagen = models.ImageField(upload_to='personas/')
    encoding = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.nombre