# Generated by Django 4.2.7 on 2023-11-20 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_framework_alter_mainbooks_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_image',
            field=models.ImageField(default='book_cover/bg2.png', null=True, upload_to='languages/'),
        ),
    ]
