# Generated by Django 5.0 on 2024-01-12 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_remove_product_digital'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='digital',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]