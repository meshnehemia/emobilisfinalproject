# Generated by Django 4.2.7 on 2023-11-30 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0021_remove_bookbought_number_remove_bookbought_receipt_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookbought',
            name='number',
            field=models.IntegerField(default=5656980),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bookbought',
            name='receipt',
            field=models.CharField(default='lkkk', max_length=30),
            preserve_default=False,
        ),
    ]
