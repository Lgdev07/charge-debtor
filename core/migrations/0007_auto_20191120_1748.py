# Generated by Django 2.2.7 on 2019-11-20 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20191120_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='debtor',
            name='last_email_sent',
            field=models.DateField(blank=True, null=True),
        ),
    ]
