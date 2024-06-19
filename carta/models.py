from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class Item(models.Model):
    nombre = models.CharField(max_length=50, null=False)
    precio = models.FloatField(null=False)
    cantidad_stock = models.IntegerField(null=False, verbose_name="Cantidad en stock")
    categoria = models.ForeignKey(Categoria, on_delete= models.CASCADE, null=True)
    foto = models.ImageField(blank=True, default="/empty.png", upload_to='items/',verbose_name="foto")

    # @property
    # def get_foto_url(self):
    #     if self.foto and hasattr(self.foto, 'url'):
    #         return self.foto.url
    #     else:
    #         return "/static/imagenes/empty.jpg"
        
    def __str__(self):
        return self.nombre
    
class Cliente(models.Model):
    dni = models.IntegerField(max_length=8, unique=True, null=False)
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento")
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre +', '+ self.apellido

class Pedido(models.Model):
    items = models.ManyToManyField(Item, blank=True, related_name="items", through='PedidoItem')
    monto_total = models.FloatField(null=False, default=0, verbose_name="Monto total")
    fecha = models.DateTimeField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    
    def calcular_monto(self):
        monto_total = 0
        for item in self.pedido_item.all():
            monto_total += item.item.precio * item.cantidad_seleccionada
        self.monto_total = monto_total
        self.save(update_fields=['monto_total'])
        return monto_total

    # def save(self):
    #     self.calcular_monto()
    #     super.save()
    
    def __str__(self):
        return f"Pedido {self.id}"

class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="pedido_item")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    cantidad_seleccionada = models.IntegerField(null=False, default=1, verbose_name="Cantidad seleccionada")

    def save(self, *args, **kwargs):
        super().save()
        self.pedido.calcular_monto()

    def delete(self, *args, **kwargs):
        pedido = self.pedido
        super().delete(*args, **kwargs)
        pedido.calcular_monto()

    def __str__(self):
        return f"{self.cantidad_seleccionada} cantidad seleccionada de {self.item.nombre} en Pedido {self.pedido.id}"

class Reserva(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    cantidad_personas = models.IntegerField(null=False, verbose_name="Cantidad de personas")
    fecha_hora = models.DateTimeField(null=False, verbose_name="Fecha y hora")

class Descuento(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    porcentaje = models.FloatField(null=True)
# Create your models here.
