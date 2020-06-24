# Generated by Django 2.2.1 on 2020-06-19 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiguracionPDF',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(blank=True, null=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('fondo', models.ImageField(blank=True, null=True, upload_to='formatoPDF/')),
            ],
        ),
        migrations.CreateModel(
            name='VisitanteSC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.TextField(blank=True, null=True)),
                ('last_name', models.TextField(blank=True, null=True)),
                ('password', models.TextField(blank=True)),
                ('curp_rfc', models.CharField(blank=True, max_length=18, null=True)),
                ('calle', models.TextField(blank=True, null=True)),
                ('noexterior', models.IntegerField(blank=True, null=True)),
                ('nointerior', models.IntegerField(blank=True, null=True)),
                ('codigopostal', models.IntegerField(blank=True, null=True)),
                ('municipio', models.TextField(blank=True, null=True)),
                ('colonia', models.TextField(blank=True, null=True)),
                ('celular', models.TextField(blank=True, null=True)),
                ('email', models.TextField(unique=True)),
                ('leida', models.CharField(default='0', max_length=1)),
                ('tipo_usuario', models.CharField(default='5', max_length=1)),
                ('tipo_persona', models.CharField(default='1', max_length=1)),
                ('inst_cct', models.TextField(blank=True, null=True)),
                ('inst_nombredirector', models.TextField(blank=True, null=True)),
                ('sector', models.TextField(blank=True, null=True)),
                ('nivel_educativo', models.CharField(blank=True, max_length=1, null=True)),
                ('modalidad', models.CharField(default='0', max_length=1, null=True)),
            ],
        ),
    ]