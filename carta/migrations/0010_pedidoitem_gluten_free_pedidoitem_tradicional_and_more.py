# Generated by Django 4.0.3 on 2024-08-07 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carta', '0009_pedido_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidoitem',
            name='gluten_free',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pedidoitem',
            name='tradicional',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pedidoitem',
            name='veggie',
            field=models.BooleanField(default=False),
        ),
    ]
