# Generated by Django 4.2.5 on 2023-09-22 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qrcode_check', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qrcodegenerator',
            name='secret_key',
            field=models.CharField(default='<function uuid4 at 0x0000024A2338D3A0>', max_length=255, unique=True, verbose_name='secret_key_string'),
        ),
    ]
