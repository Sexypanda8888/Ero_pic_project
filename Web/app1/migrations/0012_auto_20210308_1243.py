# Generated by Django 3.1.6 on 2021-03-08 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0011_auto_20210308_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='img',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='user_1',
            name='last_vote_date',
            field=models.DateField(null=True),
        ),
    ]
