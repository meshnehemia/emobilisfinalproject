# Generated by Django 4.2.7 on 2023-11-30 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0022_bookbought_number_bookbought_receipt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookbought',
            name='number',
            field=models.CharField(max_length=20),
        ),
    ]