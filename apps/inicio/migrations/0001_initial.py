# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-18 19:35
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.')], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('foto', models.ImageField(blank=True, default=b'', null=True, upload_to=b'imagenes')),
                ('telefono', models.BigIntegerField(blank=True, null=True)),
                ('estado', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'auth_user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AsigCiencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='AsigCurso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='AsigRol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Carrera',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cuerpo_msg', models.CharField(max_length=1000)),
                ('from_usuario', models.ForeignKey(db_column=b'from_usuario', on_delete=django.db.models.deletion.CASCADE, related_name='from_usuario', to=settings.AUTH_USER_MODEL)),
                ('to_usuario', models.ForeignKey(db_column=b'to_usuario', on_delete=django.db.models.deletion.CASCADE, related_name='to_usuario', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ciencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='ControlTema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(blank=True, null=True)),
                ('razon', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='CursoCatedratico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicio.Curso')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Facultad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('descripcion', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Inscripcion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(blank=True, null=True)),
                ('carrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicio.Carrera')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Invitacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Respuesta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', tinymce.models.HTMLField(blank=True)),
                ('imagen', models.ImageField(blank=True, default=b'', upload_to=b'imagen_respuesta')),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(blank=True, max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Tema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', tinymce.models.HTMLField()),
                ('imagen', models.ImageField(blank=True, default=b'', upload_to=b'imagenes')),
                ('fecha_creacion', models.DateField(blank=True)),
                ('no_respuestas', models.BigIntegerField(blank=True, null=True)),
                ('estado', models.BigIntegerField(blank=True, null=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TemaCarrera',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicio.Carrera')),
                ('tema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicio.Tema')),
            ],
        ),
        migrations.CreateModel(
            name='TemaCiencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ciencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicio.Ciencia')),
                ('tema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicio.Tema')),
            ],
        ),
        migrations.CreateModel(
            name='TemaFacultad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facultad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicio.Facultad')),
                ('tema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicio.Tema')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='rol',
            unique_together=set([('nombre', 'descripcion')]),
        ),
        migrations.AddField(
            model_name='respuesta',
            name='tema',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicio.Tema'),
        ),
        migrations.AddField(
            model_name='respuesta',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='invitacion',
            name='tema',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicio.Tema'),
        ),
        migrations.AddField(
            model_name='invitacion',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='facultad',
            unique_together=set([('nombre', 'descripcion')]),
        ),
        migrations.AddField(
            model_name='controltema',
            name='tema',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicio.Tema'),
        ),
        migrations.AddField(
            model_name='controltema',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='carrera',
            name='facultad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicio.Facultad'),
        ),
        migrations.AddField(
            model_name='asigrol',
            name='rol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicio.Rol'),
        ),
        migrations.AddField(
            model_name='asigrol',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='asigcurso',
            name='carrera',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicio.Carrera'),
        ),
        migrations.AddField(
            model_name='asigcurso',
            name='curso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicio.Curso'),
        ),
        migrations.AddField(
            model_name='asigciencia',
            name='ciencia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicio.Ciencia'),
        ),
        migrations.AddField(
            model_name='asigciencia',
            name='curso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicio.Curso'),
        ),
        migrations.AlterUniqueTogether(
            name='temafacultad',
            unique_together=set([('facultad', 'tema')]),
        ),
        migrations.AlterUniqueTogether(
            name='temaciencia',
            unique_together=set([('ciencia', 'tema')]),
        ),
        migrations.AlterUniqueTogether(
            name='temacarrera',
            unique_together=set([('carrera', 'tema')]),
        ),
        migrations.AlterUniqueTogether(
            name='invitacion',
            unique_together=set([('tema', 'usuario')]),
        ),
        migrations.AlterUniqueTogether(
            name='inscripcion',
            unique_together=set([('carrera', 'usuario')]),
        ),
        migrations.AlterUniqueTogether(
            name='cursocatedratico',
            unique_together=set([('curso', 'usuario')]),
        ),
        migrations.AlterUniqueTogether(
            name='controltema',
            unique_together=set([('tema', 'usuario')]),
        ),
        migrations.AlterUniqueTogether(
            name='carrera',
            unique_together=set([('nombre', 'facultad')]),
        ),
        migrations.AlterUniqueTogether(
            name='asigrol',
            unique_together=set([('rol', 'usuario')]),
        ),
    ]
