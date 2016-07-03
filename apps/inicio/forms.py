from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Tema, Rol, Facultad, Carrera, Ciencia,AsigCiencia,AsigRol, AsigCurso,Invitacion,Inscripcion,ControlTema,Curso,CursoCatedratico,TemaCarrera,TemaCiencia,TemaFacultad,Respuesta,User,AbstractUser


class form_addtema(forms.ModelForm):
    class Meta:
        model = Tema
        fields = ['titulo', 'descripcion', 'imagen']



class form_addrol(forms.ModelForm):
    class Meta:
        model = Rol
        fields = ['nombre', 'descripcion']


class CrearUsuario(UserCreationForm):
    admin = forms.BooleanField(required=False)
    admintienda = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ("username", "first_name",   "email", "foto", "telefono","password1", "password2", "admin", "admintienda")

    def save(self, commit=True):
        user = super(CrearUsuario, self).save(commit=False)
        user.is_staff = self.cleaned_data["admintienda"]
        user.is_superuser = self.cleaned_data["admin"]
        if commit:
            user.save()
        return user

class form_addfacu(forms.ModelForm):
    class Meta:
        model = Facultad
        fields = ['nombre', 'descripcion']

class form_carrera(forms.ModelForm):
    facultad = forms.ModelChoiceField(queryset=Facultad.objects.all(), required=True)

    class Meta:
        model = Carrera
        fields = ['facultad', 'nombre', 'descripcion']

class form_addcurso(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nombre', 'descripcion']

class form_addciencia(forms.ModelForm):
    class Meta:
        model = Ciencia
        fields = ['nombre', 'descripcion']

class form_control_Tema(forms.ModelForm):
    class Meta:
        model = ControlTema
        fields = ['razon']


class form_asignacion(forms.ModelForm):
    carrera = forms.ModelChoiceField(queryset=Carrera.objects.all(), required=True)

    class Meta:
        model = Inscripcion
        fields = ['carrera']

class form_asigCiencia(forms.ModelForm):
    curso = forms.ModelChoiceField(queryset=Curso.objects.all(), required=True)
    ciencia = forms.ModelChoiceField(queryset=Ciencia.objects.all(), required=True)

    class Meta:
        model = AsigCiencia
        fields = ['curso', 'ciencia']

class form_asig_curso(forms.ModelForm):
    curso = forms.ModelChoiceField(queryset=Curso.objects.all(), required=True)
    carrera = forms.ModelChoiceField(queryset=Carrera.objects.all(), required = True)

    class Meta:
        model = AsigCurso
        fields = ['carrera', 'curso']

class form_asig_rol(forms.ModelForm):
    nombre = forms.ModelChoiceField(queryset=Rol.objects.all(), required=True)

    class Meta:
        model = AsigRol
        fields = ['nombre']



class form_editperfil(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name",  "email", "foto", "telefono")



class form_respuesta(forms.ModelForm):
    class Meta:
        model = Respuesta
        fields = ["descripcion", "imagen"]


class form_invitacion(forms.ModelForm):
    usuario = forms.ModelChoiceField(queryset=User.objects.all(), required=True)
    class Meta:
        model = Invitacion
        fields = ["usuario"]


class form_asig_facultad(forms.ModelForm):
    facultad = forms.ModelChoiceField(queryset=Facultad.objects.all(), required=True)
    class Meta:
        model = TemaFacultad
        fields = ["facultad"]

class form_asig_carrera(forms.ModelForm):
    carrera = forms.ModelChoiceField(queryset=Carrera.objects.all(), required=True)
    class Meta:
        model = TemaCarrera
        fields = ["carrera"]


class form_asig_ciencia(forms.ModelForm):
    ciencia = forms.ModelChoiceField(queryset=Ciencia.objects.all(), required=True)
    class Meta:
        model = TemaCiencia
        fields = ["ciencia"]


class form_curso_cat(forms.ModelForm):
    curso = forms.ModelChoiceField(queryset=Curso.objects.all(), required=True)
    class Meta:
        model = CursoCatedratico
        fields = ["curso"]
