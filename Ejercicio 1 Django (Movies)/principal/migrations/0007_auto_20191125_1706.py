# Generated by Django 2.2.7 on 2019-11-25 16:06

from django.db import migrations, models
import principal.models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0006_auto_20191125_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pelicula',
            name='categoria',
            field=models.CharField(choices=[(principal.models.categoria('unknown'), 'unknown'), (principal.models.categoria('action'), 'action'), (principal.models.categoria('adventure'), 'adventure'), (principal.models.categoria('anomiation'), 'anomiation'), (principal.models.categoria('children`s'), 'children`s'), (principal.models.categoria('comedy'), 'comedy'), (principal.models.categoria('crime'), 'crime'), (principal.models.categoria('documental'), 'documental'), (principal.models.categoria('drama'), 'drama'), (principal.models.categoria('fantasy'), 'fantasy'), (principal.models.categoria('fil-noir'), 'fil-noir'), (principal.models.categoria('horror'), 'horror'), (principal.models.categoria('musica'), 'musica'), (principal.models.categoria('mystery'), 'mystery'), (principal.models.categoria('romance'), 'romance'), (principal.models.categoria('sci-fi'), 'sci-fi'), (principal.models.categoria('thriller'), 'thriller'), (principal.models.categoria('war'), 'war'), (principal.models.categoria('western'), 'western')], max_length=15),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='categoria_preferida',
            field=models.CharField(choices=[(principal.models.categoria('unknown'), 'unknown'), (principal.models.categoria('action'), 'action'), (principal.models.categoria('adventure'), 'adventure'), (principal.models.categoria('anomiation'), 'anomiation'), (principal.models.categoria('children`s'), 'children`s'), (principal.models.categoria('comedy'), 'comedy'), (principal.models.categoria('crime'), 'crime'), (principal.models.categoria('documental'), 'documental'), (principal.models.categoria('drama'), 'drama'), (principal.models.categoria('fantasy'), 'fantasy'), (principal.models.categoria('fil-noir'), 'fil-noir'), (principal.models.categoria('horror'), 'horror'), (principal.models.categoria('musica'), 'musica'), (principal.models.categoria('mystery'), 'mystery'), (principal.models.categoria('romance'), 'romance'), (principal.models.categoria('sci-fi'), 'sci-fi'), (principal.models.categoria('thriller'), 'thriller'), (principal.models.categoria('war'), 'war'), (principal.models.categoria('western'), 'western')], max_length=15),
        ),
    ]
