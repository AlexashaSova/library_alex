# Generated by Django 3.0.6 on 2020-06-01 20:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0006_auto_20200601_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='id_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mysite.Category'),
        ),
    ]
