# Generated by Django 3.2.23 on 2023-11-09 22:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialmedia', '0002_auto_20231110_0048'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='Topic',
            new_name='topic',
        ),
    ]
