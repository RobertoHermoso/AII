# Generated by Django 2.2.7 on 2019-11-24 19:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(help_text='Nombre')),
                ('apellidos', models.TextField(help_text='Apellidos')),
                ('biografia', models.TextField(help_text='Biografía')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(help_text='Nombre')),
                ('apellidos', models.TextField(help_text='Apellidos')),
                ('fecha_de_nacimiento', models.TextField(help_text='Fecha de nacimiento')),
                ('categoria_preferida', models.TextField(help_text='Tu categoría preferida')),
            ],
        ),
        migrations.CreateModel(
            name='Pelicula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.TextField(help_text='Nombre')),
                ('aapellidos', models.TextField(help_text='Apellidos')),
                ('resumen', models.TextField(help_text='Resumen de la pelicula')),
                ('categoria', models.TextField(help_text='Tu categoría preferida')),
                ('director', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='principal.Director')),
            ],
        ),
    ]