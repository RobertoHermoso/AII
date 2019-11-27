# Generated by Django 2.2.7 on 2019-11-25 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0008_auto_20191125_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pelicula',
            name='categoria',
            field=models.CharField(choices=[('UN', 'unknown'), ('AC', 'action'), ('AD', 'adventure'), ('AN', 'anomiation'), ('CH', 'children`s'), ('CO', 'comedy'), ('CR', 'crime'), ('DO', 'documental'), ('DR', 'drama'), ('FA', 'fantasy'), ('FN', 'fil-noir'), ('HO', 'horror'), ('MU', 'musica'), ('MY', 'mystery'), ('RO', 'romance'), ('SF', 'sci-fi'), ('TH', 'thriller'), ('WA', 'war'), ('WE', 'western')], max_length=15),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='categoria_preferida',
            field=models.CharField(choices=[('UN', 'unknown'), ('AC', 'action'), ('AD', 'adventure'), ('AN', 'anomiation'), ('CH', 'children`s'), ('CO', 'comedy'), ('CR', 'crime'), ('DO', 'documental'), ('DR', 'drama'), ('FA', 'fantasy'), ('FN', 'fil-noir'), ('HO', 'horror'), ('MU', 'musica'), ('MY', 'mystery'), ('RO', 'romance'), ('SF', 'sci-fi'), ('TH', 'thriller'), ('WA', 'war'), ('WE', 'western')], max_length=15),
        ),
    ]