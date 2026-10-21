from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    sku = models.CharField(max_length=50, unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    precio_unitario = models.IntegerField()
    stock = models.IntegerField()
    requiere_refrigeracion = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} ({self.sku})"

class Pedido(models.Model):
    MODALIDADES = [
        ('PICKUP', 'Retiro en Tienda'),
        ('EXPRESS', 'Despacho Express'),
    ]

    nombre_cliente = models.CharField(max_length=150)
    email_cliente = models.EmailField()
    modalidad = models.CharField(max_length=10, choices=MODALIDADES)
    fecha_entrega = models.DateField()
    direccion = models.CharField(max_length=255)
    total_estimado = models.IntegerField()
    observaciones = models.TextField(blank=True, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Pedido de {self.nombre_cliente} - {self.modalidad}"