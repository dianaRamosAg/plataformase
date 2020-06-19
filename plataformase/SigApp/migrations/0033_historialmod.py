# Generated by Django 2.2.1 on 2020-05-20 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SigApp', '0032_auto_20200508_0146'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistorialMod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechamod', models.DateTimeField()),
                ('usuario_dep', models.CharField(max_length=200)),
                ('usuario_mod', models.CharField(max_length=200)),
                ('clave_centrotrabajo_prev', models.CharField(max_length=200)),
                ('direccion_prev', models.CharField(max_length=200)),
                ('director_prev', models.CharField(max_length=200)),
                ('nombre_institucion_prev', models.CharField(max_length=200)),
                ('municipio_prev', models.CharField(max_length=200)),
                ('localidad_prev', models.CharField(max_length=200)),
                ('status_prev', models.CharField(max_length=200)),
                ('clave_centrotrabajo_new', models.CharField(max_length=200)),
                ('direccion_new', models.CharField(max_length=200)),
                ('director_new', models.CharField(max_length=200)),
                ('nombre_institucion_new', models.CharField(max_length=200)),
                ('municipio_new', models.CharField(max_length=200)),
                ('localidad_new', models.CharField(max_length=200)),
                ('status_new', models.CharField(max_length=200)),
            ],
        ),
    ]
