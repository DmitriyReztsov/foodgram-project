# Generated by Django 2.2.22 on 2021-05-25 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recepies', '0010_auto_20210525_2245'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient',
            old_name='unit',
            new_name='dimension',
        ),
    ]
