# Generated by Django 3.2 on 2021-05-02 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0011_auto_20210502_1737'),
    ]

    operations = [
        migrations.AddField(
            model_name='billdetails',
            name='product_price',
            field=models.FloatField(default=0),
        ),
    ]
