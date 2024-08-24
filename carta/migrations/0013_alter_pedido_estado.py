# Generated by Django 4.0.3 on 2024-08-12 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carta', '0012_alter_pedido_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='estado',
            field=models.CharField(choices=[('confirmado', 'confirmado'), ('preparacion', 'En preparación'), ('listo_para_entregar', 'Listo para entregar'), ('finalizado', 'Finalizado'), ('cancelado', 'Cancelado')], default='confirmado', max_length=25, verbose_name='Estado del Pedido'),
        ),
    ]