# Generated by Django 4.0.3 on 2024-06-12 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carta', '0004_alter_item_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='foto',
            field=models.ImageField(blank=True, default='/empty.png', upload_to='items/', verbose_name='foto'),
        ),
    ]
