# Generated by Django 4.2.7 on 2023-11-30 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0018_alter_bookbought_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsersPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userpk', models.IntegerField()),
                ('receipt', models.CharField(max_length=30)),
                ('number', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='bookbought',
            name='number',
        ),
        migrations.RemoveField(
            model_name='bookbought',
            name='receipt',
        ),
    ]
