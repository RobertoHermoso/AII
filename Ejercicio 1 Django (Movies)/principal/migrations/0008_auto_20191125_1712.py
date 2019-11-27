# Generated by Django 2.2.7 on 2019-11-25 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0007_auto_20191125_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pelicula',
            name='categoria',
            field=models.CharField(choices=[('unknown', 'UN'), ('action', 'AC'), ('adventure', 'AD'), ('anomiation', 'AN'), ('children`s', 'CH'), ('comedy', 'CO'), ('crime', 'CR'), ('documental', 'DO'), ('drama', 'DR'), ('fantasy', 'FA'), ('fil-noir', 'FN'), ('horror', 'HO'), ('musica', 'MU'), ('mystery', 'MY'), ('romance', 'RO'), ('sci-fi', 'SF'), ('thriller', 'TH'), ('war', 'WA'), ('western', 'WE')], max_length=15),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='categoria_preferida',
            field=models.CharField(choices=[('unknown', 'UN'), ('action', 'AC'), ('adventure', 'AD'), ('anomiation', 'AN'), ('children`s', 'CH'), ('comedy', 'CO'), ('crime', 'CR'), ('documental', 'DO'), ('drama', 'DR'), ('fantasy', 'FA'), ('fil-noir', 'FN'), ('horror', 'HO'), ('musica', 'MU'), ('mystery', 'MY'), ('romance', 'RO'), ('sci-fi', 'SF'), ('thriller', 'TH'), ('war', 'WA'), ('western', 'WE')], max_length=15),
        ),
    ]