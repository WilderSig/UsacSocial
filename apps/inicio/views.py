import os
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter,legal
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from django.db import  connection
from django.shortcuts import render, render_to_response, RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from FASE3 import settings
from .models import Tema, Rol, User, Facultad, TemaCarrera,Carrera,Ciencia,Curso,Chat,Respuesta,AsigCiencia,AsigCurso,AsigRol,ControlTema,CursoCatedratico,Inscripcion,Invitacion,TemaCiencia,TemaFacultad
from .forms import form_addtema, form_addrol, CrearUsuario, form_addfacu, form_carrera, form_addcurso, form_addciencia, form_control_Tema, form_asignacion
from .forms import form_asigCiencia, form_asig_curso, form_asig_rol, form_editperfil, form_respuesta, form_invitacion, form_asig_carrera, form_asig_ciencia, form_asig_facultad, form_curso_cat
import time

# Create your views here.


def iniciar_sesion(request):
    message = ''
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/profile')
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    return HttpResponseRedirect('/profile')
                else:
                    return HttpResponseRedirect('/normal')
            else:
                message = "Datos Incorrectos"
                return HttpResponseRedirect('/')


    else:

        formulario = AuthenticationForm()
    return render_to_response('inicio/index.html', {'formulario': formulario}, context_instance=RequestContext(request))



def nousuario(request):
    return render_to_response('404.html', context_instance=RequestContext(request))



@login_required(login_url='/iniciar_sesion/')
def privado(request):
    usuario = request.user
    if usuario.is_staff:
        return render_to_response('administrador/perfil.html', {'usuario': usuario}, context_instance=RequestContext(request))
    else:
		return render_to_response('administrador/usuario.html', {'usuario': usuario}, context_instance=RequestContext(request))


#@login_required(login_url='/iniciar_sesion/')
#def normal(request):
 #   usuario= request.user
  #  return render_to_response('usuario/perfil.html', {'usuario': usuario}, context_instance=RequestContext(request))

@login_required(login_url='/iniciar_sesion/')
def cerrar(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/iniciar_sesion/')
def profile(request):
    if not request.user.is_anonymous():
        usuario = request.user
        id_user = User.objects.get(username=request.user)
        carreras = Inscripcion.objects.filter(usuario_id = id_user.id).values('id','carrera_id__nombre','carrera_id__facultad_id__nombre')
        roles = AsigRol.objects.filter(usuario_id= id_user.id).values('id','rol_id__nombre')

        temas = Tema.objects.filter(usuario_id = id_user).values('id', 'titulo', 'fecha_creacion', 'no_respuestas','estado','usuario_id__first_name')
        tema_carr = TemaCarrera.objects.all()
        tema_cie = TemaCiencia.objects.all()
        tema_fac = TemaFacultad.objects.all()
        print(tema_fac)
        return render_to_response('administrador/perfil.html', {'tema_facultad': tema_fac, 'tema_ciencia': tema_cie ,'tema_carrera': tema_carr, 'roles': roles,'usuario': usuario, 'temas': temas, 'carreras': carreras}, context_instance=RequestContext(request))


#AGREGAR TEMA

@login_required(login_url='/iniciar_sesion/')
def crear_tema(request):
    usuario = request.user
    id_user = User.objects.get(username=request.user)
    carreras = Inscripcion.objects.filter(usuario_id=id_user).values('id','carrera_id__nombre',
                                                                     'carrera_id__facultad_id__nombre')
    roles = AsigRol.objects.filter(usuario_id=id_user.id).values('id', 'rol_id__nombre')
    if request.POST:
        formulario = form_addtema(request.POST, request.FILES)
        if formulario.is_valid():
            post = formulario.save(commit=False)

            if request.FILES:
                print(request.FILES['imagen'])
                f = request.FILES['imagen']
                post.imagen = os.path.join(settings.attachment_folder, formulario.cleaned_data['imagen'].name)
            else:
                f = ''
                post.imagen = 'imagen_tema/sinimagen.jpg'


            post.usuario_id = id_user.id
            post.fecha_creacion = time.strftime("20%y-%m-%d")
            post.estado = 1;
            post.no_respuestas = 0;
            post.save()
            handle_uploaded_file(f)
            return HttpResponseRedirect('/addtema')
    else:
        formulario = form_addtema()
        message = "Image uploaded succesfully!"
        return render_to_response('administrador/crear_tema.html', {'roles': roles,'formulario': formulario, 'usuario':usuario, 'carreras': carreras},
                                      context_instance=RequestContext(request))



@login_required(login_url='/iniciar_sesion/')
def edit_tema(request, id_tema):
    usuario = request.user
    carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre',
                                                                     'carrera_id__facultad_id__nombre')
    roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
    temas = Tema.objects.get(id=id_tema)
    if request.POST:
        formulario = form_addtema(request.POST, request.FILES, instance=temas)
        if formulario.is_valid():
            post = formulario.save(commit=False)
            if request.FILES:
                f = request.FILES['imagen']
                print(f)
                handle_uploaded_file(f)
                post.imagen = os.path.join(settings.attachment_folder, formulario.cleaned_data['imagen'].name)
            else:
                f = ''
                post.imagen = 'imagen_tema/sinimagen.jpg'
                handle_uploaded_file(f)
            post.no_respuestas = 0;
            post.save()

            return HttpResponseRedirect('/profile')
    else:
        formulario = form_addtema(instance=temas)
        message = "Image uploaded succesfully!"
        return render_to_response('administrador/edit_tema.html', {'roles': roles,'formulario': formulario, 'usuario':usuario, 'carreras': carreras},
                                      context_instance=RequestContext(request))



@login_required(login_url='/iniciar_sesion/')
def eliminar_tema(request, id_tema):
    temas=Tema.objects.get(id=id_tema)
    temas.delete()
    return HttpResponseRedirect("/profile")


#ROLES
@login_required(login_url='/iniciar_sesion/')
def crear_rol(request):
    usuario = request.user

    carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre',
                                                                     'carrera_id__facultad_id__nombre')
    roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
    message = None
    if request.user.is_staff:
        if request.POST:
            formulario = form_addrol(request.POST)
            if formulario.is_valid:
                formulario.save()
                message = "Registro completado con exito"
                return HttpResponseRedirect('/addrol')

        else:
            formulario = form_addrol()
        return render_to_response('administrador/crear_rol.html', {'roles':roles,'formulario': formulario, 'usuario': usuario, 'carreras': carreras, 'message': message } ,
                                      context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')

#CRUD ROLES

@login_required(login_url='/iniciar_sesion/')
def mostrarRol(request):

    if not request.user.is_staff:
        return HttpResponseRedirect('/nousuario')
    else:
        rol = Rol.objects.all()
        usuario = request.user

        carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre',
                                                                     'carrera_id__facultad_id__nombre')
        roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
        return render_to_response('administrador/rol.html', {'roles':roles, 'rol':rol,'usuario': usuario, 'carreras': carreras})

@login_required(login_url='/iniciar_sesion/')
def eliminar_rol(request, id_rol):
    if request.user.is_staff:
        roles=Rol.objects.get(id=id_rol)
        roles.delete()
        message= 'Rol eliminado Exitosamente'
        return HttpResponseRedirect("/rol")
    else:
        return render_to_response('administrador/rol.html')

@login_required(login_url='/iniciar_sesion/')
def editar_rol(request, id_rol):
    usuario = request.user

    carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre',
                                                                     'carrera_id__facultad_id__nombre')
    roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
    if request.user.is_staff:
        roles=Rol.objects.get(id =id_rol)
        if request.method=="POST":
            formulario=form_addrol(request.POST, instance=roles)
            if formulario.is_valid():
                formulario.save()
                return HttpResponseRedirect("/rol")
        else:
            formulario = form_addrol(instance=roles)
            return render_to_response("administrador/edit_rol.html",{'roles': roles,"formulario":formulario, "usuario": usuario, 'carreras':carreras},context_instance=RequestContext(request))
    else:
        HttpResponseRedirect('/nousuario')

#CRUD USUARIOS
@login_required(login_url='/iniciar_sesion/')
def mostrarTablaUsuario(request):

    if not request.user.is_staff:
        return HttpResponseRedirect("/nousuario")
    else:
        usuarios = User.objects.all()
        usuario = request.user
        carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre','carrera_id__facultad_id__nombre')
        roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
        return render_to_response('administrador/usuario.html', {'roles': roles,'usuarios':usuarios, "usuario": usuario, 'carreras':carreras})


@login_required(login_url='/iniciar_sesion/')
def eliminar_usuario(request, id_usuario):
    if request.user.is_staff:
        usuarios=User.objects.get(id=id_usuario)
        usuarios.delete()
        return HttpResponseRedirect("/usuarios")
    else:
        return render_to_response('administrador/usuario.html')



@login_required(login_url='/iniciar_sesion/')
def nuevo_usuario(request):
    usuario = request.user

    carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre',
                                                                     'carrera_id__facultad_id__nombre')
    roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
    if request.POST:
        form = CrearUsuario(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            if (request.FILES):
                    f = request.FILES['foto']
                    user.foto = os.path.join(settings.attachment_folder, form.cleaned_data['foto'].name)
                    handle_uploaded_file(f)

            else:
                if (request.POST['foto'] == ''):
                    user.foto = 'sinfoto.jpg'
                    f = ''
                    handle_uploaded_file(f)

            user.passw = request.POST.get('password1')
            user.admin = request.POST.get('admin', False)
            user.save()



            # succes_url = reverse_lazy('reportarusuario')
            return HttpResponseRedirect('/adduser')
            # return render_to_response('autores/reportarUsuario.html')
            # message = "usuario registrado"
    else:
        form = CrearUsuario()

    args = {}
    args.update(csrf(request))

    args['form'] = form
    args['usuario'] = usuario
    args['carreras'] = carreras
    args['roles'] = roles
    return render_to_response("administrador/crear_user.html", args,
                              context_instance=RequestContext(request))



@login_required(login_url='/iniciar_sesion/')
def editar_usuario(request, id_usuario):
    usuario = request.user
    usuarios = User.objects.get(id=id_usuario)

    carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre',
                                                                     'carrera_id__facultad_id__nombre')
    roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
    if request.POST:
        form = CrearUsuario(request.POST, request.FILES, instance=usuarios)
        if form.is_valid():
            user = form.save(commit=False)
            if(request.FILES):
                if (request.FILES['foto'] != ''):
                    print(request.FILES['foto'])
                    f = request.FILES['foto']
                    user.foto = os.path.join(settings.attachment_folder, form.cleaned_data['foto'].name)
                    handle_uploaded_file(f)
                else:
                    f = ''
                    user.foto = 'sinfoto.jpg'
                    handle_uploaded_file(f)
            else:
                try:
                    if(request.POST['foto-clear']):
                        user.foto = 'sinfoto.jpg'
                except:
                    user.foto = usuarios.foto


            user.admin = request.POST.get('admin', False)
            user.save()
            # succes_url = reverse_lazy('reportarusuario')
            return HttpResponseRedirect('/usuarios')
            # return render_to_response('autores/reportarUsuario.html')
            # message = "usuario registrado"
    else:
        form = CrearUsuario(instance=usuarios)

    args = {}
    args.update(csrf(request))

    args['formulario'] = form
    args['usuario'] = usuario
    args['carreras'] = carreras
    args['roles'] = roles
    return render_to_response("administrador/edit_user.html", args,
                              context_instance=RequestContext(request))






#@login_required(login_url='/iniciar_sesion/')
#def editar_usuario(request, id_usuario):
 #   if request.user.is_staff:
  #      usuario=request.user

   #     usuarios=User.objects.get(id =id_usuario)
    #    if request.method=="POST":

     #       formulario=CrearUsuario(request.POST, instance=usuarios)
      #      if formulario.is_valid():
       #         formulario.save()
     #           return HttpResponseRedirect("/usuarios")
        #else:
         #   formulario = CrearUsuario(instance=usuarios)
          #  return render_to_response("administrador/edit_user.html",{"formulario":formulario, "usuario": usuario},context_instance=RequestContext(request))
   # else:
    #    return HttpResponseRedirect('/nousuario')


#GUARDA LA IMAGEN
def handle_uploaded_file(f):
    if(f!=''):
        file_name = os.path.join(settings.attachment_path, f.name) # acordate del settings.py poner lodel attachement_path
        destination = open(file_name, 'wb+')
        for chunk in f.chunks():
             destination.write(chunk)
        destination.close()
    else:
        print('Sin imagen')

#FACULTADES
@login_required(login_url='/iniciar_sesion/')
def mostrarFac(request):

    if not request.user.is_staff:

        return HttpResponseRedirect('/nousuario')

    else:

        facultades = Facultad.objects.all()
        usuario = request.user

        carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre','carrera_id__facultad_id__nombre')
        roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
        return render_to_response('administrador/facultad.html', {'roles': roles ,'facultades':facultades, 'usuario': usuario, 'carreras': carreras})



@login_required(login_url='/iniciar_sesion/')
def crear_facultad(request):
    usuario = request.user

    carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre',
                                                                     'carrera_id__facultad_id__nombre')
    roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
    message = None
    if request.user.is_staff:
        if request.POST:
            formulario = form_addfacu(request.POST)
            if formulario.is_valid:
                formulario.save()
                message = "Registro completado con exito"
                return HttpResponseRedirect('/addfac')

        else:
            formulario = form_addrol()
        return render_to_response('administrador/crear_facultad.html', {'roles': roles,'carreras': carreras,'formulario': formulario, 'usuario': usuario, 'message': message } ,
                                      context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


@login_required(login_url='/iniciar_sesion/')
def eliminar_fac(request, id_fac):
    if request.user.is_staff:
        facultades=Facultad.objects.get(id=id_fac)
        facultades.delete()
        message= 'Rol eliminado Exitosamente'
        return HttpResponseRedirect("/facultades")
    else:
        return render_to_response('administrador/facultades.html')

@login_required(login_url='/iniciar_sesion/')
def editar_fac(request, id_fac):
    usuario = request.user
    carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre',
                                                                        'carrera_id__facultad_id__nombre')
    roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
    if request.user.is_staff:
        facultades=Facultad.objects.get(id =id_fac)
        if request.method=="POST":
            formulario=form_addfacu(request.POST, instance=facultades)
            if formulario.is_valid():
                formulario.save()
                return HttpResponseRedirect("/facultades")
        else:
            formulario = form_addrol(instance=facultades)
            return render_to_response("administrador/edit_facultad.html",{'roles': roles,'carreras': carreras,"formulario":formulario, "usuario": usuario},context_instance=RequestContext(request))
    else:
        HttpResponseRedirect('/nousuario') #pagina de acceso denegado


#CARRERAS

@login_required(login_url='/iniciar_sesion/')
def mostrarCarrera(request):

    if not request.user.is_staff:
        return HttpResponseRedirect("/nousuario")
    else:

        carre = Carrera.objects.all().values('id', 'nombre', 'descripcion','facultad_id__nombre')
        usuario = request.user
        carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre',
                                                                        'carrera_id__facultad_id__nombre')
        roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
        return render_to_response('administrador/carreras.html', {'roles':roles,'carre':carre, 'usuario': usuario, 'carreras': carreras})



@login_required(login_url='/iniciar_sesion/')
def crear_carrera(request):
    usuario = request.user
    carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre',
                                                                        'carrera_id__facultad_id__nombre')
    roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
    if request.user.is_staff:
        if request.POST:
            formulario = form_carrera(request.POST)
            if formulario.is_valid:
                formulario.save()
                return HttpResponseRedirect('/addcarrera')
        else:
            formulario = form_carrera()
            return render_to_response('administrador/crear_carrera.html', {'roles': roles,'carreras': carreras,'formulario': formulario, 'usuario': usuario},
                                      context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/nousuario') #pagina acceso denegado



@login_required(login_url='/iniciar_sesion/')
def eliminar_carrera(request, id_carrera):
    if request.user.is_staff:
        carreras=Carrera.objects.get(id=id_carrera)
        carreras.delete()
        return HttpResponseRedirect("/carreras")
    else:
        return render_to_response('administrador/carreras.html')


@login_required(login_url='/iniciar_sesion/')
def editar_carrera(request, id_carrera):
    usuario =  request.user
    carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre',
                                                                        'carrera_id__facultad_id__nombre')
    roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
    if request.user.is_staff:
        carre=Carrera.objects.get(id =id_carrera)
        if request.method=="POST":
            formulario=form_carrera(request.POST, instance=carre)
            if formulario.is_valid():
                formulario.save()
                return HttpResponseRedirect("/carreras")
        else:
            formulario = form_carrera(instance=carre)
            return render_to_response("administrador/edit_carrera.html",{'roles':roles,'carreras': carreras,"formulario":formulario, 'usuario': usuario},context_instance=RequestContext(request))
    else:
        HttpResponseRedirect('/nousuario') #acceso denegado

#CRUD CURSOS


@login_required(login_url='/iniciar_sesion/')
def MostrarCurso(request):

    if not request.user.is_staff:
        HttpResponseRedirect("/nousuario")

    else:

        cursos = Curso.objects.all()

        usuario = request.user
        carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre',
                                                                        'carrera_id__facultad_id__nombre')
        roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
        return render_to_response('administrador/cursos.html', {'roles': roles,'carreras': carreras,'cursos':cursos, 'usuario': usuario})

@login_required(login_url='/iniciar_sesion/')
def eliminar_curso(request, id_curso):
    if request.user.is_staff:
        cursos=Curso.objects.get(id=id_curso)
        cursos.delete()
        message= 'Curso eliminado Exitosamente'
        return HttpResponseRedirect("/cursos")
    else:
        return render_to_response('administrador/cursos.html')

@login_required(login_url='/iniciar_sesion/')
def editar_curso(request, id_curso):
    usuario = request.user
    carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre',
                                                                        'carrera_id__facultad_id__nombre')
    roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
    if request.user.is_staff:
        cursos=Curso.objects.get(id =id_curso)
        if request.method=="POST":
            formulario=form_addcurso(request.POST, instance=cursos)
            if formulario.is_valid():
                formulario.save()
                return HttpResponseRedirect("/cursos")
        else:
            formulario = form_addcurso(instance=cursos)
            return render_to_response("administrador/edit_curso.html",{'roles':roles,'carreras':carreras,"formulario":formulario, "usuario": usuario},context_instance=RequestContext(request))
    else:
        HttpResponseRedirect('/nousuario')

@login_required(login_url='/iniciar_sesion/')
def crear_curso(request):
    usuario = request.user
    carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre',
                                                                        'carrera_id__facultad_id__nombre')
    roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
    message = None
    if request.user.is_staff:
        if request.POST:
            formulario = form_addcurso(request.POST)
            if formulario.is_valid:
                formulario.save()
                message = "Registro completado con exito"
                return HttpResponseRedirect('/addcurso')

        else:
            formulario = form_addcurso()
        return render_to_response('administrador/crear_curso.html', {'roles':roles,'carreras':carreras,'formulario': formulario, 'usuario': usuario, 'message': message } ,
                                      context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/nousario')




#CRUD CIENCIAS


@login_required(login_url='/iniciar_sesion/')
def MostrarCiencia(request):

    if not request.user.is_staff:
        return HttpResponseRedirect("/nousuario")
    else:
        ciencias = Ciencia.objects.all()
        usuario = request.user
        carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre',
                                                                        'carrera_id__facultad_id__nombre')
        roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
        return render_to_response('administrador/ciencias.html', {'roles': roles,'carreras':carreras,'ciencias':ciencias, 'usuario': usuario})

@login_required(login_url='/iniciar_sesion/')
def eliminar_ciencia(request, id_ciencia):
    if request.user.is_staff:
        ciencias=Ciencia.objects.get(id=id_ciencia)
        ciencias.delete()
        message= 'Ciencia eliminado Exitosamente'
        return HttpResponseRedirect("/ciencias")
    else:
        return render_to_response('administrador/ciencias.html')

@login_required(login_url='/iniciar_sesion/')
def editar_ciencia(request, id_ciencia):
    usuario = request.user
    carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre',
                                                                        'carrera_id__facultad_id__nombre')
    roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
    if request.user.is_staff:
        ciencias=Ciencia.objects.get(id =id_ciencia)
        if request.method=="POST":
            formulario=form_addciencia(request.POST, instance=ciencias)
            if formulario.is_valid():
                formulario.save()
                return HttpResponseRedirect("/ciencias")
        else:
            formulario = form_addciencia(instance=ciencias)
            return render_to_response("administrador/edit_ciencia.html",{'roles':roles,'carreras': carreras,"formulario":formulario, "usuario": usuario},context_instance=RequestContext(request))
    else:
        HttpResponseRedirect('/nousuario')

@login_required(login_url='/iniciar_sesion/')
def crear_ciencia(request):
    usuario = request.user
    carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre',
                                                                        'carrera_id__facultad_id__nombre')
    roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
    message = None
    if request.user.is_staff:
        if request.POST:
            formulario = form_addciencia(request.POST)
            if formulario.is_valid:
                formulario.save()
                message = "Registro completado con exito"
                return HttpResponseRedirect('/addciencia')

        else:
            formulario = form_addciencia()
        return render_to_response('administrador/crear_ciencia.html', {'roles':roles,'carreras':carreras,'formulario': formulario, 'usuario': usuario, 'message': message } ,
                                      context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/nousario')


#TEMAS


@login_required(login_url='/iniciar_sesion/')
def MostrarTemas(request):

    temas = Tema.objects.all().values('id', 'titulo', 'descripcion', 'fecha_creacion', 'no_respuestas','estado','usuario_id__first_name')
    usuario = request.user
    carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre',
                                                                        'carrera_id__facultad_id__nombre')
    roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
    return render_to_response('administrador/temas.html', {'roles':roles,'carreras': carreras,'temas':temas, 'usuario': usuario})


@login_required(login_url='/iniciar_sesion/')
def editar_ciencia(request, id_ciencia):
    usuario = request.user
    carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre',
                                                                        'carrera_id__facultad_id__nombre')
    roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
    if request.user.is_staff:
        ciencias=Ciencia.objects.get(id =id_ciencia)
        if request.method=="POST":
            formulario=form_addciencia(request.POST, instance=ciencias)
            if formulario.is_valid():
                formulario.save()
                return HttpResponseRedirect("/ciencias")
        else:
            formulario = form_addciencia(instance=ciencias)
            return render_to_response("administrador/edit_ciencia.html",{'roles':roles,'carreras':carreras,"formulario":formulario, "usuario": usuario},context_instance=RequestContext(request))
    else:
        HttpResponseRedirect('/nousuario')


#SOLUCIONAR TEMAS


@login_required(login_url='/iniciar_sesion/')
def solucionar_tema(request, id_tema):
    tema = Tema.objects.get(id = id_tema)
    id_user = User.objects.get(username=request.user)
    usuario = request.user
    carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre',
                                                                        'carrera_id__facultad_id__nombre')
    roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
    if request.method=="POST":
        formulario=form_control_Tema(request.POST)
        if formulario.is_valid():
            post = formulario.save(commit=False)
            post.usuario_id = id_user.id
            post.fecha = time.strftime("20%y-%m-%d")
            post.tema_id = id_tema
            post.save()
            tema.estado = 0
            tema.save()
            return HttpResponseRedirect('/gene_temas')
    else:
        formulario = form_control_Tema()
        return render_to_response("administrador/sol_tema.html",{'roles': roles,'carreras':carreras,"formulario":formulario, "usuario": usuario, 'tema': tema},context_instance=RequestContext(request))




#--------------------------------------------REACTIVAR TEMA-------------------------------------


@login_required(login_url='/iniciar_sesion/')
def reactivar_tema(request, id_tema):
    tema = Tema.objects.get(id = id_tema)
    tema_control = ControlTema.objects.get(tema = id_tema)
    usuario = request.user
    carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre',
                                                                        'carrera_id__facultad_id__nombre')
    roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
    tema_control.delete()
    tema.estado = 1
    tema.save()
    return HttpResponseRedirect('/gene_temas')





#INSCRIPCION


@login_required(login_url='/iniciar_sesion/')
def inscripcion(request):
    usuario = request.user
    message = ''
    id_user = User.objects.get(username=request.user)
    carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre',
                                                                        'carrera_id__facultad_id__nombre')
    roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
    if request.POST:

        formulario = form_asignacion(request.POST)
        if formulario.is_valid:
            form = formulario.save(commit=False)
            form.usuario_id = id_user.id
            form.fecha = time.strftime("20%y-%m-%d")
            carrera = request.POST['carrera']
            inscrip = Inscripcion.objects.filter(usuario=id_user.id, carrera=carrera);
            if inscrip:
                print('Ya se inscribio a esta carrera')
            else:
                form.save()
                print('Inscrito Exitosamente!')
            message = 'Asignado Exitosamente'
            return HttpResponseRedirect('/asig_carr')

    else:

        formulario = form_asignacion()

    return render_to_response('administrador/asig_carrera.html', {'roles': roles,'carreras':carreras,'formulario': formulario, 'usuario': usuario, 'message': message},
                                      context_instance=RequestContext(request))




@login_required(login_url='/iniciar_sesion/')
def asig_ciencia(request):
    usuario = request.user
    carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre',
                                                                        'carrera_id__facultad_id__nombre')
    roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
    message= None
    if request.user.is_staff:

        if request.POST:

            formulario = form_asigCiencia(request.POST)
            if formulario.is_valid:
                curso = request.POST['curso']
                ciencia = request.POST['ciencia']

                ciencia_curso = AsigCiencia.objects.filter(curso=curso, ciencia=ciencia);
                if ciencia_curso:
                    print('Ciencia y curso ya estan asignados')
                else:
                    formulario.save()
                    print('Ciencia Asignada Exitosamente!')
                message = 'Asignado Exitosamente'
                return HttpResponseRedirect('/asig_ciencia')

        else:

            formulario = form_asigCiencia()

        return render_to_response('administrador/asig_ciencia.html', {'roles': roles,'carreras':carreras,'formulario': formulario, 'usuario': usuario, 'message': message},
                                      context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/nousuario') #pagina acceso denegado


@login_required(login_url='/iniciar_sesion/')
def asig_curso(request):
    usuario = request.user
    carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre',
                                                                        'carrera_id__facultad_id__nombre')
    roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
    message= None
    if request.user.is_staff:

        if request.POST:

            formulario = form_asig_curso(request.POST)
            if formulario.is_valid:
                curso = request.POST['curso']
                carrera = request.POST['carrera']

                curso_carrera = AsigCurso.objects.filter(curso=curso, carrera = carrera);
                if curso_carrera:
                    print('Carrera y curso ya estan asignados')
                else:
                    formulario.save()
                    print('Curso Asignado Exitosamente!')
                message = 'Asignado Exitosamente'
                return HttpResponseRedirect('/asig_curso')

        else:

            formulario = form_asig_curso()

        return render_to_response('administrador/asig_curso.html', {'roles':roles,'carreras':carreras,'formulario': formulario, 'usuario': usuario, 'message': message},
                                      context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/nousuario') #pagina acceso denegado



@login_required(login_url='/iniciar_sesion/')
def asig_rol(request):
    usuario = request.user
    carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre',
                                                                        'carrera_id__facultad_id__nombre')
    roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
    message = ''
    id_user = User.objects.get(username=request.user)


    if request.POST:

        formulario = form_asig_rol(request.POST)
        if formulario.is_valid:
            form = formulario.save(commit=False)
            form.usuario_id = id_user.id
            rol = request.POST['nombre']
            print(rol)
            form.rol_id = rol
            inscrip = AsigRol.objects.filter(usuario=id_user.id, rol=rol);
            print(inscrip)
            if inscrip:
                print('Ya se asigno este rol')
            else:
                form.save()
                print('Rol Asignado exitosamente!')
            message = 'Asignado Exitosamente'
            return HttpResponseRedirect('/asig_rol')

    else:
        formulario = form_asig_rol()

    return render_to_response('administrador/asig_rol.html',
                                  {'roles':roles ,'carreras':carreras,'formulario': formulario, 'usuario': usuario, 'message': message},
                                  context_instance=RequestContext(request))


@login_required(login_url='/iniciar_sesion/')
def eliminar_asignacion(request, id_inscrip):
        Inscripciones=Inscripcion.objects.get(id=id_inscrip)
        Inscripciones.delete()
        print('Inscripcion eliminado Exitosamente')
        return HttpResponseRedirect('/profile')

@login_required(login_url='/iniciar_sesion/')
def eliminar_asig_rol(request, id_asig_rol):
        Asignacion_rol=AsigRol.objects.get(id=id_asig_rol)
        Asignacion_rol.delete()
        print('Asignacion eliminado Exitosamente')
        return HttpResponseRedirect('/profile')





@login_required(login_url='/iniciar_sesion/')
def MostrarControl(request):

    temas = ControlTema.objects.all().values('id', 'tema_id__titulo', 'fecha', 'razon','usuario_id__first_name')
    usuario = request.user
    carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre',
                                                                        'carrera_id__facultad_id__nombre')
    roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
    return render_to_response('administrador/control_tema.html', {'roles':roles,'carreras': carreras,'temas':temas, 'usuario': usuario})



#DISCUSION DE TEMAS



@login_required(login_url='/iniciar_sesion/')
def tema_discusion(request, id_tema):
    usuario = request.user
    id_user = User.objects.get(username=request.user)
    carreras = Inscripcion.objects.filter(usuario_id = id_user.id).values('id','carrera_id__nombre','carrera_id__facultad_id__nombre')
    roles = AsigRol.objects.filter(usuario_id= id_user.id).values('id','rol_id__nombre')
    respuestas = Respuesta.objects.filter(tema_id = id_tema).values('descripcion', 'imagen','usuario_id__first_name', 'usuario_id__email','usuario_id__foto')
    temas = Tema.objects.filter(id = id_tema).values('id', 'titulo', 'fecha_creacion', 'no_respuestas','estado','usuario_id__first_name','usuario_id__email' , 'descripcion','usuario_id__foto', 'imagen')
    if request.POST:
        formulario = form_respuesta(request.POST, request.FILES)
        respues = formulario.save(commit=False)
        fechas = Tema.objects.get(id = id_tema)
        fechas.no_respuestas = fechas.no_respuestas + 1
        fechas.save()
        respues.usuario_id = usuario.id
        respues.tema_id = id_tema
        respues.save()
        return HttpResponseRedirect('/foro/'+id_tema)
    else:
        return render_to_response('administrador/tema_discusion.html', {'respuestas': respuestas,'roles': roles,'usuario': usuario, 'temas': temas, 'carreras': carreras}, context_instance=RequestContext(request))

    return render_to_response('usuario/tema_discusion.html', {'respuestas': respuestas,'usuario': usuario}, context_instance=RequestContext(request))





@login_required(login_url='/iniciar_sesion/')
def editar_perfil(request, id_usuario):
    usuario = request.user
    usuarios = User.objects.get(id=id_usuario)

    carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre',
                                                                     'carrera_id__facultad_id__nombre')
    roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
    if request.POST:
        form = form_editperfil(request.POST, request.FILES, instance=usuarios)
        if form.is_valid():
            user = form.save(commit=False)
            if(request.FILES):
                if (request.FILES['foto'] != ''):
                    print(request.FILES['foto'])
                    f = request.FILES['foto']
                    user.foto = os.path.join(settings.attachment_folder, form.cleaned_data['foto'].name)
                    handle_uploaded_file(f)
                else:
                    f = ''
                    user.foto = 'sinfoto.jpg'
                    handle_uploaded_file(f)
            else:
                try:
                    if(request.POST['foto-clear']):
                        user.foto = 'sinfoto.jpg'
                except:
                    user.foto = usuarios.foto



            user.save()
            # succes_url = reverse_lazy('reportarusuario')
            return HttpResponseRedirect('/profile')
            # return render_to_response('autores/reportarUsuario.html')
            # message = "usuario registrado"
    else:
        form = form_editperfil(instance=usuarios)

    args = {}
    args.update(csrf(request))

    args['formulario'] = form
    args['usuario'] = usuario
    args['carreras'] = carreras
    args['roles'] = roles
    return render_to_response("administrador/editar_perfil.html", args,
                              context_instance=RequestContext(request))





@login_required(login_url='/iniciar_sesion/')
def tema_facultad(request, id_tema):
    usuario = request.user
    carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre',
                                                                        'carrera_id__facultad_id__nombre')
    roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
    if request.POST:
        formulario = form_asig_facultad(request.POST)
        if formulario.is_valid:
            fac_tema = formulario.save(commit=False)
            facult = request.POST['facultad']
            fac_tema.tema_id = id_tema
            ciencia_curso = TemaFacultad.objects.filter(facultad=facult, tema=id_tema);
            if ciencia_curso:
                print('Ya invitada')
            else:
                fac_tema.save()
                print('Facultad invitada exitosamente!')

            return HttpResponseRedirect('/tema_facu/'+id_tema)

    else:
        formulario = form_asig_facultad()
    return render_to_response('administrador/tema_facultad.html', {'roles': roles,'carreras':carreras,'formulario': formulario, 'usuario': usuario},
                                      context_instance=RequestContext(request))





@login_required(login_url='/iniciar_sesion/')
def tema_usuario(request, id_tema):
    usuario = request.user
    carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre',
                                                                        'carrera_id__facultad_id__nombre')
    roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
    if request.POST:
        formulario = form_invitacion(request.POST)
        if formulario.is_valid:
            user_form = formulario.save(commit=False)
            user = request.POST['usuario']
            user_form.tema_id = id_tema
            user_invitacion = Invitacion.objects.filter(usuario=user, tema=id_tema);
            if user_invitacion:
                print('Ya invitada')
            else:
                user_form.save()
                print('Usuario invitado exitosamente!')

            return HttpResponseRedirect('/asignacion_tema/'+id_tema)

    else:
        formulario = form_invitacion()
    return render_to_response('administrador/asig_tema.html', {'roles': roles,'carreras':carreras,'formulario': formulario, 'usuario': usuario},
                                      context_instance=RequestContext(request))




@login_required(login_url='/iniciar_sesion/')
def tema_carrera(request, id_tema):
    usuario = request.user
    carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre',
                                                                        'carrera_id__facultad_id__nombre')
    roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
    if request.POST:
        formulario = form_asig_carrera(request.POST)
        if formulario.is_valid:
            carr_form = formulario.save(commit=False)
            carrera = request.POST['carrera']
            carr_form.tema_id = id_tema
            carrera_Tema = TemaCarrera.objects.filter(carrera=carrera, tema=id_tema);
            if carrera_Tema:
                print('Ya invitada')
            else:
                carr_form.save()
                print('Carrera invitada exitosamente!')

            return HttpResponseRedirect('/asig_carrera/'+id_tema)

    else:
        formulario = form_asig_carrera()
    return render_to_response('administrador/tema_carrera.html', {'roles': roles,'carreras':carreras,'formulario': formulario, 'usuario': usuario},
                                      context_instance=RequestContext(request))



@login_required(login_url='/iniciar_sesion/')
def tema_ciencia(request, id_tema):
    usuario = request.user
    carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre',
                                                                        'carrera_id__facultad_id__nombre')
    roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
    if request.POST:
        formulario = form_asig_ciencia(request.POST)
        if formulario.is_valid:
            cien_form = formulario.save(commit=False)
            ciencia = request.POST['ciencia']
            cien_form.tema_id = id_tema
            ciencia_Tema = TemaCiencia.objects.filter(ciencia=ciencia, tema=id_tema);
            if ciencia_Tema:
                print('Ya invitada')
            else:
                cien_form.save()
                print('Carrera invitada exitosamente!')

            return HttpResponseRedirect('/asig_ciencia/'+id_tema)

    else:
        formulario = form_asig_ciencia()
    return render_to_response('administrador/tema_ciencia.html', {'roles': roles,'carreras':carreras,'formulario': formulario, 'usuario': usuario},
                                      context_instance=RequestContext(request))





#----------------------------------------REPORTE CATEDRATICOS-------------------------

@login_required(login_url='/iniciar_sesion/')
def reporte_catedraticos(request, id_tema):
    print "Generando Reporte en PDF"
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "Profesores.pdf"  # llamado clientes
    # la linea 26 es por si deseas descargar el pdf a tu computadora
    #response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,

                            pagesize=(landscape(legal)),
                            rightMargin=0,
                            leftMargin=00,
                            topMargin=00,
                            bottomMargin=00,
                            )
    clientes = []
    styles = getSampleStyleSheet()
    header = Paragraph("Profesores con mas respuestas", styles['Heading1'])
    clientes.append(header)
    headings = ('TITULO DE TEMA','USUARIO','NOMBRE', 'CANTIDAD DE RESPUESTAS')


    cursor = connection.cursor()
    cursor.execute("""
    SELECT  T.TITULO , U.USERNAME REGISTRO , U.FIRST_NAME NOMBRE , COUNT(R.USUARIO_ID) AS NO_RESPUESTAS
FROM INICIO_RESPUESTA R, AUTH_USER U, INICIO_TEMA T, INICIO_ROL RO, INICIO_ASIGROL ASR
WHERE U.ID = R.USUARIO_ID
AND R.TEMA_ID = T.ID
AND T.ID = %s
AND ASR.USUARIO_ID = U.ID
AND RO.ID = ASR.ROL_ID
AND RO.NOMBRE = 'Catedratico'
AND ROWNUM <= 5
GROUP BY U.USERNAME, U.FIRST_NAME, T.TITULO
ORDER BY NO_RESPUESTAS DESC
""", [id_tema])
    resultados = cursor.fetchall()
    resultsList = []
    for row in resultados:
        resultsList.append(row)


    print resultsList
    t = Table([headings] + resultsList)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (9, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.azure),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)

        ]
    ))
    clientes.append(t)
    doc.build(clientes)
    response.write(buff.getvalue())
    buff.close()
    return response

#-------------------------------------------REPORTE ESTUDIANTES--------------------------------

@login_required(login_url='/iniciar_sesion/')
def reporte_estudiantes(request, id_tema):
    print "Generando Reporte en PDF"
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "Estudiantes.pdf"  # llamado clientes
    # la linea 26 es por si deseas descargar el pdf a tu computadora
    #response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,

                            pagesize=(landscape(legal)),
                            rightMargin=0,
                            leftMargin=00,
                            topMargin=00,
                            bottomMargin=00,
                            )
    clientes = []
    styles = getSampleStyleSheet()
    header = Paragraph("Estudiantes con mas respuestas en este tema", styles['Heading1'])
    clientes.append(header)
    headings = ('TITULO DE TEMA','USUARIO','NOMBRE', 'CANTIDAD DE RESPUESTAS')


    cursor = connection.cursor()
    cursor.execute("""
    SELECT U.USERNAME , U.FIRST_NAME , COUNT(R.USUARIO_ID) AS CANTI_RESPUES, T.TITULO
FROM INICIO_RESPUESTA R, AUTH_USER U, INICIO_TEMA T, INICIO_ROL RO, INICIO_ASIGROL ASR
WHERE U.ID = R.USUARIO_ID
AND R.TEMA_ID = T.ID
AND T.ID = %s
AND ASR.USUARIO_ID = U.ID
AND RO.ID = ASR.ROL_ID
AND RO.NOMBRE = 'Estudiante'
AND ROWNUM <= 3
GROUP BY U.USERNAME, U.FIRST_NAME, T.TITULO
ORDER BY CANTI_RESPUES DESC
""", [id_tema])
    resultados = cursor.fetchall()
    resultsList = []
    for row in resultados:
        resultsList.append(row)


    print resultsList
    t = Table([headings] + resultsList)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (9, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.azure),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)

        ]
    ))
    clientes.append(t)
    doc.build(clientes)
    response.write(buff.getvalue())
    buff.close()
    return response



#---------------------------------------------AGRUPADOS POR CIENCIA----------------------------

@login_required(login_url='/iniciar_sesion/')
def reporte_3(request):
    print "Generando Reporte en PDF"
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "Reporte3.pdf"  # llamado clientes
    # la linea 26 es por si deseas descargar el pdf a tu computadora
    #response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,

                            pagesize=(landscape(legal)),
                            rightMargin=0,
                            leftMargin=00,
                            topMargin=00,
                            bottomMargin=00,
                            )
    clientes = []
    styles = getSampleStyleSheet()
    header = Paragraph("Top 5 de temas que mas respuesta tienen, agrupados por ciencia", styles['Heading1'])
    clientes.append(header)
    headings = ('TITULO DE TEMA','FECHA DE CREACION', 'CANTIDAD DE RESPUESTAS', 'ESTADO', 'AUTOR', 'CIENCIA')


    cursor = connection.cursor()
    cursor.execute("""
    SELECT  T.TITULO,T.FECHA_CREACION,T.NO_RESPUESTAS,T.ESTADO, U.FIRST_NAME AUTOR, C.NOMBRE  CIENCIA
FROM INICIO_TEMA T, AUTH_USER U, INICIO_CIENCIA C, INICIO_TEMACIENCIA TC
WHERE T.USUARIO_ID = U.ID
AND TC.TEMA_ID = T.ID
AND TC.CIENCIA_ID = C.ID
AND ROWNUM <= 5
ORDER BY T.NO_RESPUESTAS DESC
""")
    resultados = cursor.fetchall()
    resultsList = []
    for row in resultados:
        resultsList.append(row)


    print resultsList
    t = Table([headings] + resultsList)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (9, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.azure),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)

        ]
    ))
    clientes.append(t)
    doc.build(clientes)
    response.write(buff.getvalue())
    buff.close()
    return response







@login_required(login_url='/iniciar_sesion/')
def Mostrar_Reporte3(request):
        usuario = request.user
        carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id', 'carrera_id__nombre',
                                                                        'carrera_id__facultad_id__nombre')
        roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
        cursor = connection.cursor()
#---------------------------------TEMAS POR CIENCIA CON MAS RESPUESTAS ------------------------------------
        cursor.execute("""
SELECT  T.TITULO, T.DESCRIPCION,T.FECHA_CREACION,T.NO_RESPUESTAS,T.ESTADO, U.FIRST_NAME AUTOR, C.NOMBRE  CIENCIA
FROM INICIO_TEMA T, AUTH_USER U, INICIO_CIENCIA C, INICIO_TEMACIENCIA TC
WHERE T.USUARIO_ID = U.ID
AND TC.TEMA_ID = T.ID
AND TC.CIENCIA_ID = C.ID
AND ROWNUM <= 5
ORDER BY T.NO_RESPUESTAS DESC
""")
        resultados = cursor.fetchall()
        resultsList = []
        x = cursor.description
        for row in resultados:
            i= 0
            dato = {}
            while i < len(x):
                dato[x[i][0]] = row[i]
                i = i+1
            resultsList.append(dato)
#----------------------------------------------------TEMAS ORDENADOS POR FECHA -----------------------------------
            cursor1 = connection.cursor()
            cursor1.execute("""
        SELECT  T.TITULO, T.DESCRIPCION,T.FECHA_CREACION,T.NO_RESPUESTAS,T.ESTADO, U.FIRST_NAME AUTOR
        FROM INICIO_TEMA T, AUTH_USER U
        WHERE T.USUARIO_ID = U.ID
        ORDER BY T.FECHA_CREACION DESC
        """)
            resultado = cursor1.fetchall()
            resultsList1 = []
            x = cursor1.description
            for row in resultado:
                i = 0
                datito = {}
                while i < len(x):
                    datito[x[i][0]] = row[i]
                    i = i + 1
                resultsList1.append(datito)
        return render_to_response('administrador/reportes.html', {'reporte4': resultsList1,"reporte3":resultsList, 'carreras':carreras,'roles':roles,'usuario':usuario}, context_instance=RequestContext(request))




#--------------------------------------------GENERAR REPORTE 4---------------------------------



@login_required(login_url='/iniciar_sesion/')
def reporte_4(request):
    print "Generando Reporte en PDF"
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "TemasOrdenados.pdf"  # llamado clientes
    # la linea 26 es por si deseas descargar el pdf a tu computadora
    #response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,

                            pagesize=(landscape(legal)),
                            rightMargin=0,
                            leftMargin=00,
                            topMargin=00,
                            bottomMargin=00,
                            )
    clientes = []
    styles = getSampleStyleSheet()
    header = Paragraph("Temas ordenados por fecha", styles['Heading1'])
    clientes.append(header)
    headings = ('TITULO DE TEMA','FECHA DE CREACION', 'CANTIDAD DE RESPUESTAS', 'ESTADO', 'AUTOR')


    cursor = connection.cursor()
    cursor.execute("""
    SELECT  T.TITULO,T.FECHA_CREACION,T.NO_RESPUESTAS,T.ESTADO, U.FIRST_NAME AUTOR
FROM INICIO_TEMA T, AUTH_USER U
WHERE T.USUARIO_ID = U.ID
ORDER BY T.FECHA_CREACION DESC
""")
    resultados = cursor.fetchall()
    resultsList = []
    for row in resultados:
        resultsList.append(row)


    print resultsList
    t = Table([headings] + resultsList)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (9, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.azure),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)

        ]
    ))
    clientes.append(t)
    doc.build(clientes)
    response.write(buff.getvalue())
    buff.close()
    return response




#----------------------------------------------------REPORTE 1-------------------------------------------------------------






@login_required(login_url='/iniciar_sesion/')
def Mostrar_Reporte1(request,id_tema):
        usuario = request.user
        carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id', 'carrera_id__nombre',
                                                                        'carrera_id__facultad_id__nombre')
        roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
        cursor = connection.cursor()


        cursor.execute("""
            SELECT U.USERNAME , U.FIRST_NAME , COUNT(R.USUARIO_ID) AS CANTI_RESPUES, T.TITULO
        FROM INICIO_RESPUESTA R, AUTH_USER U, INICIO_TEMA T, INICIO_ROL RO, INICIO_ASIGROL ASR
        WHERE U.ID = R.USUARIO_ID
        AND R.TEMA_ID = T.ID
        AND T.ID = %s
        AND ASR.USUARIO_ID = U.ID
        AND RO.ID = ASR.ROL_ID
        AND RO.NOMBRE = 'Estudiante'
        AND ROWNUM <= 3
        GROUP BY U.USERNAME, U.FIRST_NAME, T.TITULO
        ORDER BY CANTI_RESPUES DESC
        """, [id_tema])
        resultados = cursor.fetchall()
        resultsList = []
        x = cursor.description
        for row in resultados:
            i= 0
            dato = {}
            while i < len(x):
                dato[x[i][0]] = row[i]
                i = i+1
            resultsList.append(dato)

        return render_to_response('administrador/reporte1.html', {"reporte1":resultsList, 'carreras':carreras,'roles':roles,'usuario':usuario}, context_instance=RequestContext(request))




@login_required(login_url='/iniciar_sesion/')
def MostrarReporte2(request,id_tema):
        usuario = request.user
        carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id', 'carrera_id__nombre',
                                                                        'carrera_id__facultad_id__nombre')
        roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
        cursor = connection.cursor()


        cursor.execute("""
            SELECT U.USERNAME , U.FIRST_NAME , COUNT(R.USUARIO_ID) AS CANTI_RESPUES, T.TITULO
        FROM INICIO_RESPUESTA R, AUTH_USER U, INICIO_TEMA T, INICIO_ROL RO, INICIO_ASIGROL ASR
        WHERE U.ID = R.USUARIO_ID
        AND R.TEMA_ID = T.ID
        AND T.ID = %s
        AND ASR.USUARIO_ID = U.ID
        AND RO.ID = ASR.ROL_ID
        AND RO.NOMBRE = 'Estudiante'
        AND ROWNUM <= 3
        GROUP BY U.USERNAME, U.FIRST_NAME, T.TITULO
        ORDER BY NO_RESPUESTAS DESC
        """, [id_tema])
        resultados = cursor.fetchall()
        resultsList = []
        x = cursor.description
        for row in resultados:
            i= 0
            dato = {}
            while i < len(x):
                dato[x[i][0]] = row[i]
                i = i+1
            resultsList.append(dato)

        return render_to_response('administrador/reporte2.html', {"reporte1":resultsList, 'carreras':carreras,'roles':roles,'usuario':usuario}, context_instance=RequestContext(request))





#---------------------------------------------CURSO CATEDRATICO-----------------------------

@login_required(login_url='/iniciar_sesion/')
def curso_catedratico(request):
    if not request.user.is_anonymous():
        usuario = request.user
        id_user = User.objects.get(username=request.user)
        carreras = Inscripcion.objects.filter(usuario_id = id_user.id).values('id','carrera_id__nombre','carrera_id__facultad_id__nombre')
        roles = AsigRol.objects.filter(usuario_id= id_user.id).values('id','rol_id__nombre')

        cursos = CursoCatedratico.objects.filter(usuario_id=id_user).values( 'id','curso_id__nombre', 'curso_id__descripcion')

        return render_to_response('administrador/curso_catedratico.html', {'roles': roles,'usuario': usuario, 'cursos': cursos, 'carreras': carreras}, context_instance=RequestContext(request))







@login_required(login_url='/iniciar_sesion/')
def asig_curso_cat(request):
    usuario = request.user
    carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre',
                                                                        'carrera_id__facultad_id__nombre')
    roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
    message = ''
    id_user = User.objects.get(username=request.user)


    if request.POST:

        formulario = form_curso_cat(request.POST)
        if formulario.is_valid:
            form = formulario.save(commit=False)
            form.usuario_id = id_user.id
            curso = request.POST['curso']
            print(curso)
            form.curso_id = curso
            inscrip = CursoCatedratico.objects.filter(usuario=id_user.id, curso=curso);
            print(inscrip)
            if inscrip:
                print('Ya se asigno este curso')
            else:
                form.save()
                print('Curso Asignado exitosamente!')
            message = 'Asignado Exitosamente'
            return HttpResponseRedirect('/curso_cat')

    else:
        formulario = form_curso_cat()

    return render_to_response('administrador/asig_rol.html',
                                  {'roles':roles ,'carreras':carreras,'formulario': formulario, 'usuario': usuario, 'message': message},
                                  context_instance=RequestContext(request))




#------------------------------------ELIMINAR ASIGNACION DE CURSO----------------------


@login_required(login_url='/iniciar_sesion/')
def eliminar_asig_curso(request, id_curso):
        Asignacion_curso=CursoCatedratico.objects.get(id=id_curso)
        Asignacion_curso.delete()
        print('Curso eliminado Exitosamente')
        return HttpResponseRedirect('/curso_cat')




@login_required(login_url='/iniciar_sesion/')
def ver_detalle(request, id_tema):
    id_user = User.objects.get(username=request.user)
    usuario = request.user
    carreras = Inscripcion.objects.filter(usuario_id=usuario.id).values('id','carrera_id__nombre',
                                                                        'carrera_id__facultad_id__nombre')
    roles = AsigRol.objects.filter(usuario_id=usuario.id).values('id', 'rol_id__nombre')
    det_facultades = TemaFacultad.objects.filter(tema_id = id_tema).values('id', 'facultad_id__nombre')
    det_carreras = TemaCarrera.objects.filter(tema_id=id_tema).values('id', 'carrera_id__nombre')
    det_ciencias = TemaCiencia.objects.filter(tema_id=id_tema).values('id', 'ciencia_id__nombre')
    det_usuarios = Invitacion.objects.filter(tema_id=id_tema).values('id', 'usuario_id__first_name')
    tema = Tema.objects.get(id=id_tema)

    formulario = form_control_Tema()
    return render_to_response("administrador/detalle_tema.html",{'tema':tema,'usuarios': det_usuarios,'ciencias': det_ciencias, 'carre': det_carreras,'facultades': det_facultades,'roles': roles,'carreras':carreras,"formulario":formulario, "usuario": usuario},context_instance=RequestContext(request))




@login_required(login_url='/iniciar_sesion/')
def eli_asig_usuario(request, id_inscrip):
        Inscripciones=Invitacion.objects.get(id=id_inscrip)
        Inscripciones.delete()
        print('Inscripcion eliminado Exitosamente')
        return HttpResponseRedirect('/gene_temas')


@login_required(login_url='/iniciar_sesion/')
def eli_asig_ciencia(request, id_inscrip):
        Inscripciones=TemaCiencia.objects.get(id=id_inscrip)
        Inscripciones.delete()
        print('Inscripcion eliminado Exitosamente')
        return HttpResponseRedirect('/gene_temas')


@login_required(login_url='/iniciar_sesion/')
def eli_asig_facultad(request, id_inscrip):
        Inscripciones=TemaFacultad.objects.get(id=id_inscrip)
        Inscripciones.delete()
        print('Inscripcion eliminado Exitosamente')
        return HttpResponseRedirect('/gene_temas')



@login_required(login_url='/iniciar_sesion/')
def eli_asig_carrera(request, id_inscrip):
        Inscripciones=TemaCarrera.objects.get(id=id_inscrip)
        Inscripciones.delete()
        print('Inscripcion eliminado Exitosamente')
        return HttpResponseRedirect('/gene_temas')