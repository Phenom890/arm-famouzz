# Generated by Django 5.0.4 on 2024-10-15 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_address_options_order_ref_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ref_code',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
