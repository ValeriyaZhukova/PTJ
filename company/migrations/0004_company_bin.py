# Generated by Django 3.1.3 on 2021-02-04 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_auto_20201227_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='bin',
            field=models.CharField(default=0, max_length=12),
            preserve_default=False,
        ),
    ]
