from django.conf.urls import url, include
from django.contrib import admin
from .views import iniciar_sesion,privado,nousuario, cerrar, profile, eliminar_tema,crear_tema,mostrarRol, crear_rol, eliminar_rol
from .views import editar_rol, mostrarTablaUsuario, nuevo_usuario, eliminar_usuario, editar_usuario, mostrarFac, crear_facultad, editar_fac,eliminar_fac
from .views import mostrarCarrera, crear_carrera, editar_carrera, eliminar_carrera,MostrarCurso, crear_curso, editar_curso, eliminar_curso
from .views import crear_ciencia,MostrarCiencia, editar_ciencia, eliminar_ciencia, MostrarTemas,edit_tema, solucionar_tema, inscripcion
from .views import asig_ciencia, asig_curso, asig_rol, eliminar_asignacion, eliminar_asig_rol,MostrarControl, tema_discusion, editar_perfil
from .views import tema_facultad,tema_usuario, tema_carrera, tema_ciencia, reporte_catedraticos, reporte_estudiantes,reporte_3
from .views import Mostrar_Reporte3, reporte_4, Mostrar_Reporte1, MostrarReporte2, reactivar_tema, curso_catedratico, asig_curso_cat, eliminar_asig_curso, ver_detalle
from .views import eli_asig_usuario, eli_asig_carrera,eli_asig_facultad, eli_asig_ciencia




urlpatterns = [
    url(r'^$', iniciar_sesion, name='loguearse'),  # paginade inicio
    url(r'^privado/$', privado ),
    url(r'^privado/$', privado ),
    url(r'^nousuario/$', nousuario),
    #url(r'^normal/$', normal),
    url(r'^cerrar/$',cerrar),
    url(r'^profile/$',profile),

    url(r'borrar_tema/(?P<id_tema>\d+)$',eliminar_tema, name="del_tema"),
    url(r'^addtema/',crear_tema, name="add_tema"),



    url(r'^rol/$', mostrarRol, name="roles"),

    url(r'^addrol/$', crear_rol, name="crear_rol"),
    url(r'delete_rol/(?P<id_rol>\d+)$',eliminar_rol, name="dele_rol"),
    url(r'edit_rol/(?P<id_rol>\d+)$',editar_rol, name="editar_rol"),

    #USUARIOS
    url(r'^usuarios/$', mostrarTablaUsuario , name="usuarios"),
    url(r'borraruser/(?P<id_usuario>\d+)$',eliminar_usuario, name="delete_user"),
    url(r'editaruser/(?P<id_usuario>\d+)$',editar_usuario, name="edit_user"),
    url(r'^adduser/$', nuevo_usuario , name="agregar_usuario"),

    #FACULTADES
    url(r'^facultades/$', mostrarFac , name="facultades"),
    url(r'^addfac/$', crear_facultad , name="add_factulad"),
    url(r'delete_fac/(?P<id_fac>\d+)$', eliminar_fac, name="delete_fac"),
    url(r'editfac/(?P<id_fac>\d+)$', editar_fac, name="edit_fac"),

    #CARRERAS
    url(r'^carreras/$', mostrarCarrera , name="facultades"),
    url(r'^addcarrera/$', crear_carrera  , name="add_factulad"),
    url(r'delete_car/(?P<id_carrera>\d+)$', eliminar_carrera, name="delete_carr"),
    url(r'edit_car/(?P<id_carrera>\d+)$', editar_carrera, name="edit_carr"),


    #CURSOS
    url(r'^cursos/$', MostrarCurso, name="cursos"),
    url(r'^addcurso/$', crear_curso, name="add_curso"),
    url(r'delete_cur/(?P<id_curso>\d+)$', eliminar_curso, name="delete_cur"),
    url(r'edit_cur/(?P<id_curso>\d+)$', editar_curso, name="edit_cur"),

    # CIENCIAS
    url(r'^ciencias/$', MostrarCiencia, name="ciencias"),
    url(r'^addciencia/$', crear_ciencia, name="add_ciencia"),
    url(r'delete_cie/(?P<id_ciencia>\d+)$', eliminar_ciencia, name="delete_ciencia"),
    url(r'edit_cie/(?P<id_ciencia>\d+)$', editar_ciencia, name="edit_ciencia"),

    #TEMAS
    url(r'^gene_temas/$', MostrarTemas, name="temas"),
    url(r'edit_tema/(?P<id_tema>\d+)$', edit_tema, name="edit_tema"),
    url(r'sol_tema/(?P<id_tema>\d+)$', solucionar_tema, name="solucionar_tema"),
    url(r're_tema/(?P<id_tema>\d+)$', reactivar_tema, name="reactivar_tema"),

    #ASIGNAR CARRERA, CURSO Y CIENCIA
    url(r'asig_carr/$', inscripcion, name="inscripcion"),
    url(r'asig_ciencia/$', asig_ciencia, name="asignar_ciencia"),
    url(r'asig_curso/$', asig_curso, name="asignar_ciencia"),
    url(r'asig_rol/$', asig_rol, name="asignar_ciencia"),

    #ELIMINAR ASIGNACION A CARRERA
    url(r'delete_inscripcion/(?P<id_inscrip>\d+)$', eliminar_asignacion, name="delete_asignacion"),
    #ELIMINAR ASIGNACION DE ROL
    url(r'del_asig_rol/(?P<id_asig_rol>\d+)$', eliminar_asig_rol, name="delete_asignacion"),

    #MOSTRAR CONTROL DE TEMAS CLAUSURADOS
    url(r'control_tema/$', MostrarControl, name="delete_asignacion"),

    #DISCUSION DE TEMAS
    url(r'foro/(?P<id_tema>\d+)$', tema_discusion, name="delete_asignacion"),

    #EDITAR PERFIL
    url(r'mi_perfil/(?P<id_usuario>\d+)$',editar_perfil , name="edit_perfil"),

    #ASIGNACION DE TEMAS
    url(r'tema_facu/(?P<id_tema>\d+)$',tema_facultad , name="edit_perfil"),
    #ASIGNACION DE USUARIOS A TEMAS
    url(r'asignacion_tema/(?P<id_tema>\d+)$',tema_usuario , name="invitacion_usuario"),
    #ASIGNACION DE TEMAS A CARRERA
    url(r'asig_carrera/(?P<id_tema>\d+)$',tema_carrera , name="invitacion_usuario"),
    #ASIGNAR CIENCIA A TEMA
    url(r'asig_ciencia/(?P<id_tema>\d+)$', tema_ciencia, name="invitacion_usuario"),

    #REPORTE 1
    url(r'RP1/(?P<id_tema>\d+)$', reporte_catedraticos, name="reporte1"),
    url(r'RP2/(?P<id_tema>\d+)$', reporte_estudiantes, name="reporte2"),

    url(r'RP3/$', reporte_3, name="reporte3"),
    url(r'RP4/$', reporte_4, name="reporte4"),


    url(r'reportes/$', Mostrar_Reporte3, name="reportes"),
    #reporte1
    url(r'ver_rep1/(?P<id_tema>\d+)$', Mostrar_Reporte1, name="reporte1"),

    #REPORTE 2
    url(r'ver_rep2/(?P<id_tema>\d+)$', MostrarReporte2, name="reporte2"),
    #CURSOS CATEDRATICO

    url(r'curso_cat/$', curso_catedratico, name="curso_Cat"),
    url(r'asig_cat/$', asig_curso_cat, name="asign_curso_Cat"),
    url(r'el_curso/(?P<id_curso>\d+)$', eliminar_asig_curso, name="eliminar_curso"),
    url(r'det_tema/(?P<id_tema>\d+)$', ver_detalle , name="eliminar_curso"),


    url(r'el_carrera/(?P<id_inscrip>\d+)$', eli_asig_carrera , name="el_Carrera"),
    url(r'el_ciencia/(?P<id_inscrip>\d+)$', eli_asig_ciencia , name="eliminar_curso"),
    url(r'el_facultad/(?P<id_inscrip>\d+)$', eli_asig_facultad , name="eliminar_curso"),
    url(r'el_user/(?P<id_inscrip>\d+)$', eli_asig_usuario , name="eliminar_curso"),




]
