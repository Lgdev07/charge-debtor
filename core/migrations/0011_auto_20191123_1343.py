# Generated by Django 2.2.7 on 2019-11-23 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_debtor_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='debtor',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Profile', verbose_name='Created By'),
        ),
    ]
