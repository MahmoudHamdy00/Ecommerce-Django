# Generated by Django 4.0.4 on 2022-05-04 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0007_alter_product_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=4, max_digits=10),
        ),
    ]