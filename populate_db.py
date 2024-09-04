import os
import django
import random
from carta.models import Item

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'menuDigital.settings')
django.setup()

# Nombres de platos aleatorios
PLATOS = [
    "Sopa de Tomate",
    "Ensalada César",
    "Bistec a la Parrilla",
    "Pasta Carbonara",
    "Tarta de Queso",
    "Helado de Vainilla",
    "Coca-Cola",
    "Sorrentinos",
    "Ravioles",
    "Empanadas de Carne",
    "Empanadas de Pollo",
    "Agua Mineral",
    "Pollo al Curry",
    "Hamburguesa",
    "Pizza Margarita",
    "Sushi",
    "Tacos",
    "Ramen",
    "Sándwich de Pavo",
    "Tiramisú",
    "Mojito",
    "Café Espresso",
    "Café Cortado",
    "Café con Leche",
    "Tostados de Jamón y Queso",
    "Medialunas",
    "Helado",
    "Muffin de Arándanos",
    "Malbec",
    "Merlot",
    "Sauvignon",
    "Cabernet",
    "Bonarda",
]

# Función para poblar la base de datos con 50 items
def populate_database():
    # Crear 50 items
    for plato in PLATOS:
        # Seleccionar un nombre de plato
        nombre = plato
        
        # Generar datos aleatorios para el item
        precio = round(random.uniform(5.0, 20.0), 2)
        cantidad_seleccionada = random.randint(0, 10)
        cantidad_stock = random.randint(10, 100)
        
        # Crear el item y guardarlo en la base de datos
        item = Item.objects.create(
            nombre=nombre,
            precio=precio,
            cantidad_seleccionada=cantidad_seleccionada,
            cantidad_stock=cantidad_stock
        )
        
        print(f"Item creado: {item.nombre}")

if __name__ == "__main__":
    populate_database()
