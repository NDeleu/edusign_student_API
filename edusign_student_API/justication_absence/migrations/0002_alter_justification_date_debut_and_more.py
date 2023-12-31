# Generated by Django 4.2.5 on 2023-09-22 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('justication_absence', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='justification',
            name='date_debut',
            field=models.DateTimeField(verbose_name='start_absence_justified_date'),
        ),
        migrations.AlterField(
            model_name='justification',
            name='date_fin',
            field=models.DateTimeField(verbose_name='end_absence_justified_date'),
        ),
    ]
