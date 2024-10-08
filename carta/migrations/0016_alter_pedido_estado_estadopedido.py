# Generated by Django 4.0.3 on 2024-08-24 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carta', '0015_alter_pedido_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='estado',
            field=models.CharField(choices=[('pendiente', 'pendiente de confirmacion'), ('confirmado', 'confirmado'), ('preparacion', 'En preparación'), ('listo_para_entregar', 'Listo para entregar'), ('entregado', 'entregado'), ('finalizado', 'Finalizado'), ('cancelado', 'Cancelado')], default='confirmado', max_length=25, verbose_name='Estado del Pedido'),
        ),
        migrations.CreateModel(
            name='EstadoPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('pendiente', 'pendiente de confirmacion'), ('confirmado', 'confirmado'), ('preparacion', 'En preparación'), ('listo_para_entregar', 'Listo para entregar'), ('entregado', 'entregado'), ('finalizado', 'Finalizado'), ('cancelado', 'Cancelado')], max_length=25)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carta.pedido')),
            ],
        ),
    ]
