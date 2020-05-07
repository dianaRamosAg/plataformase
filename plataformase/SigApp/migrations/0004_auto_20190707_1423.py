# Generated by Django 2.2.1 on 2019-07-07 20:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SigApp', '0003_detallecarrera_areainteres'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carrera',
            name='Area_Estudio',
        ),
        migrations.RemoveField(
            model_name='detallecarrera',
            name='areaInteres',
        ),
        migrations.AddField(
            model_name='carrera',
            name='areaInteres',
            field=models.ForeignKey(default=21, on_delete=django.db.models.deletion.CASCADE, to='SigApp.AreaInteres'),
            preserve_default=False,
        ),
    ]