# Generated by Django 4.2.7 on 2023-11-29 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialmedia', '0011_remove_groupmessages_receiver_groups_groupcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groups',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='groups',
            name='groupcode',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='groups',
            name='icon',
            field=models.ImageField(default='groupsicon/img_3.png', upload_to='groupsicon/'),
        ),
        migrations.AlterField(
            model_name='groups',
            name='rules',
            field=models.TextField(null=True),
        ),
    ]
