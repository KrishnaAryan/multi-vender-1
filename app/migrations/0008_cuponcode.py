# Generated by Django 4.2 on 2023-04-09 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_product_packing_cost_product_tax_alter_product_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='CuponCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('discount', models.IntegerField()),
            ],
        ),
    ]
