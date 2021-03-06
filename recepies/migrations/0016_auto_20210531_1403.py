# Generated by Django 2.2.22 on 2021-05-31 11:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recepies', '0015_shopinglist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quantityingreds',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quantityingred', to='recepies.Ingredient'),
        ),
        migrations.AlterField(
            model_name='quantityingreds',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quantityingred', to='recepies.Recipe'),
        ),
    ]
