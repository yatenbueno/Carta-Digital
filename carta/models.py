from django.db import models
from django.contrib.auth.models import BaseUserManager, User

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

    def __str__(self):
        return self.nombre


class ClienteManager(BaseUserManager):
    def create_cliente(self, username, email, password, first_name, last_name, dni, fecha_nacimiento):
        # Crear el usuario
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Crear el cliente asociado al usuario
        cliente = self.model(
            user=user,
            dni=dni,
            fecha_nacimiento=fecha_nacimiento
        )
        cliente.save(using=self._db)
        return cliente

class Cliente(models.Model):
    dni = models.CharField(max_length=8, unique=True, null=False)
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento")
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    objects = ClienteManager()

    def __str__(self):
        return f"{self.user.first_name}, {self.user.last_name}"


class Pedido(models.Model):
    Estados = [
         # ('valor_interno', 'Etiqueta visible')
        ('pendiente', 'pendiente de confirmacion'),
        ('confirmado', 'confirmado'),
        ('preparacion', 'En preparación'),
        ('listo_para_entregar', 'Listo para entregar'),
        ('entregado', 'entregado'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
        
    ]
    anotacion_cliente = models.TextField(blank= True, null= True)
    items = models.ManyToManyField(Item, blank=True, related_name="items", through='PedidoItem')
    monto_total = models.FloatField(null=False, default=0, verbose_name="Monto total")
    fecha = models.DateTimeField(null=True, auto_now_add=True)  # Definido con auto_now_add para establecer la fecha automáticamente al crear un pedido
    cliente = models.ForeignKey(Cliente, null=True, on_delete=models.CASCADE)
    completado= models.BooleanField(default=False, null=True)
    estado= models.CharField(max_length=25, choices= Estados, default= 'confirmado', verbose_name="Estado del Pedido")

    def calcular_monto(self):
        monto_total = 0
        for item in self.pedido_item.all():
            monto_total += item.item.precio * item.cantidad_seleccionada
        self.monto_total = monto_total
        self.save(update_fields=['monto_total'])
        return monto_total 
        
   
    def get_estado_display(self):
        return dict(self.Estados).get(self.estado, 'Desconocido')

    def __str__(self):
        return f'Pedido {self.id} - {self.get_estado_display()}'

class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="pedido_item")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    cantidad_seleccionada = models.IntegerField(null=False, default=1, verbose_name="Cantidad seleccionada")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Subtotal")
   

    def calcular_subtotal(self):
        self.subtotal = self.item.precio * self.cantidad_seleccionada
    
    def save(self, *args, **kwargs):
        self.calcular_subtotal()
        super().save(*args, **kwargs)
        self.pedido.calcular_monto()

    def delete(self, *args, **kwargs):
        pedido = self.pedido
        super().delete(*args, **kwargs)
        pedido.calcular_monto()

    def __str__(self):
        return f"{self.cantidad_seleccionada} cantidad seleccionada de {self.item.nombre} en Pedido {self.pedido.id}"


