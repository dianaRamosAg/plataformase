# Generated by Django 2.2.1 on 2019-10-21 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SigApp', '0014_auto_20190916_2049'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatosTemporal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clave_centrotrabajo_temp', models.CharField(max_length=30)),
                ('direccion_temp', models.CharField(max_length=250)),
                ('director_temp', models.CharField(max_length=100)),
                ('nombre_institucion', models.CharField(max_length=50)),
                ('municipio', models.CharField(max_length=30)),
                ('localidad', models.CharField(max_length=70)),
                ('status', models.CharField(max_length=15)),
                ('modificando', models.BooleanField()),
            ],
        ),
    ]