# Generated by Django 2.2.1 on 2020-06-14 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SETyRS', '0002_remove_solicitudexamen_fecha_exa'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudexamen',
            name='fecha_exa',
            field=models.DateField(blank=True, default='2020-06-06'),
        ),
    ]
