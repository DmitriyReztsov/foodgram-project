# Generated by Django 2.2.22 on 2021-05-25 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recepies', '0011_auto_20210525_2255'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient',
            old_name='dimension',
            new_name='unit',
        ),
    ]
