# Generated by Django 5.0.7 on 2024-10-18 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cse', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactus',
            name='id',
        ),
        migrations.AlterField(
            model_name='contactus',
            name='comments',
            field=models.TextField(max_length=255),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='email',
            field=models.EmailField(max_length=254, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='firstname',
            field=models.TextField(max_length=255),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='lastname',
            field=models.TextField(max_length=255),
        ),
        migrations.AlterModelTable(
            name='contactus',
            table='contactus',
        ),
    ]
