# Generated by Django 3.1.6 on 2021-03-08 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0012_auto_20210308_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='img',
            name='date',
            field=models.CharField(max_length=16, null=True),
        ),
    ]
