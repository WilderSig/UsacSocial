from django.contrib import admin
from .models import AsigCurso, AsigRol, Carrera, Chat, Ciencia, ControlTema, Curso, CursoCatedratico, Facultad,Inscripcion,Invitacion,\
    Respuesta,Rol,Tema,TemaCarrera,TemaCiencia,TemaFacultad,User

admin.site.register(AsigCurso)
admin.site.register(AsigRol)
admin.site.register(Carrera)
admin.site.register(Chat)
admin.site.register(Ciencia)
admin.site.register(ControlTema)
admin.site.register(Curso)
admin.site.register(CursoCatedratico)
admin.site.register(Facultad)
admin.site.register(Inscripcion)
admin.site.register(Invitacion)
admin.site.register(User)
admin.site.register(Respuesta)
admin.site.register(Rol)
admin.site.register(TemaFacultad)
admin.site.register(Tema)
admin.site.register(TemaCarrera)
admin.site.register(TemaCiencia)

