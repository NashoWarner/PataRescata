# Generated by Django 5.0.2 on 2024-02-28 16:08

import apppatarescata.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apppatarescata', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='email_verificado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='usuario',
            name='token_verificacion',
            field=models.CharField(default=apppatarescata.models.generar_token, max_length=40),
        ),
    ]
