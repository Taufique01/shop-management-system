# Generated by Django 3.2 on 2021-05-02 09:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_simcompanypayment'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='simcompanypayment',
            unique_together={('year', 'month')},
        ),
    ]
