# Generated by Django 2.2.24 on 2022-06-06 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appAdmin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='status_serveur',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='app',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
