# Generated by Django 3.2.4 on 2021-06-14 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funcapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funktion',
            name='errorfield',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='ошибка'),
        ),
    ]
