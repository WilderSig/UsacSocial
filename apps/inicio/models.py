from django.contrib.flatpages import models
from django.db import models
from tinymce import models as tinymce_models

from django.contrib.auth.models import AbstractUser

# Create your models here.



class Facultad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=300, blank=True, null=True)


    class Meta:
        unique_together = (('nombre', "descripcion"),)

    def __unicode__(self):
        return self.nombre



class User(AbstractUser):
    foto = models.ImageField(upload_to='imagenes', default='', null=True, blank=True)
    telefono = models.BigIntegerField(blank=True, null=True)
    estado = models.BooleanField(default=True)
    passw = models.CharField(max_length = 100, blank=True)

    class Meta:
        db_table = 'auth_user'


class Rol(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=300, blank=True)

    class Meta:
        unique_together = (('nombre', "descripcion"),)

    def __unicode__(self):
        return self.nombre



class AsigRol(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('rol', "usuario"),)




class Tema(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = tinymce_models.HTMLField()
    imagen = models.ImageField(upload_to='imagenes', default='', blank=True  )
    fecha_creacion = models.DateField(blank=True)
    no_respuestas = models.BigIntegerField(blank=True, null=True)
    estado = models.BigIntegerField(blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.titulo

class Carrera(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300,  null=True)
    facultad = models.ForeignKey(Facultad,on_delete=models.CASCADE)

    class Meta:
        unique_together = (('nombre','facultad'),)

    def __unicode__(self):
        return self.nombre

class Ciencia(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=300)

    def __unicode__(self):
        return self.nombre


class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300)

    def __unicode__(self):
        return self.nombre

class AsigCurso(models.Model):
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)




class CursoCatedratico(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('curso', 'usuario'),)

    def __unicode__(self):
        return self.carrera

class Chat(models.Model):
    cuerpo_msg = models.CharField(max_length=1000)
    from_usuario = models.ForeignKey(User,on_delete=models.CASCADE, db_column='from_usuario', related_name='from_usuario')
    to_usuario = models.ForeignKey(User, on_delete=models.CASCADE, db_column='to_usuario', related_name='to_usuario')

    def __unicode__(self):
        return  self.from_usuario

class AsigCiencia(models.Model):
    ciencia = models.ForeignKey(Ciencia, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.curso



class TemaCarrera(models.Model):
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('carrera', 'tema'),)
    def __unicode__(self):
        return self.tema


class TemaCiencia(models.Model):
    ciencia = models.ForeignKey(Ciencia, on_delete=models.CASCADE)
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('ciencia', 'tema'),)

    def __unicode__(self):
        return self.tema


class TemaFacultad(models.Model):
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE)
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('facultad', 'tema'),)


class ControlTema(models.Model):
    fecha = models.DateField(blank=True, null=True)
    razon = models.CharField(max_length=300, blank=True, null=True)
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('tema', 'usuario'),)


class Respuesta(models.Model):
    descripcion = tinymce_models.HTMLField(blank=True)
    imagen = models.ImageField(upload_to='imagen_respuesta', default='', blank=True)
    tema = models.ForeignKey('Tema', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.usuario



class Invitacion(models.Model):
    tema = models.ForeignKey(Tema,on_delete=models.CASCADE)
    usuario = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        unique_together = (('tema', 'usuario'),)


class Inscripcion(models.Model):
    fecha = models.DateField(blank=True, null=True)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('carrera', 'usuario'),)

