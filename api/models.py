from math import prod
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator


def validate_nonzero(value):
    """
    Metodo que valida cantidad de producto permitida.
    La cantidad no puede ser igual o menor  cero.
    """
    if value <= 0:
        raise ValidationError(
            ('Cantidad %(value)s no permitida'),
            params={'value': value},
        )


class Product(models.Model):
    """
    Modelo que representa una instancia de Producto
    """
    name = models.CharField(max_length=250)
    price = models.FloatField()
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Order(models.Model):
    """
    Modelo que representa una instancia de Orden
    """
    date_time = models.DateTimeField()

    def __str__(self):
        return f'Orden número: ' + str(self.id) + '. Fecha: ' \
            + str(self.date_time)


class OrderDetail(models.Model):
    """
    Modelo que representa una instancia de Detalle de una orden
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    cuantity = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(999), validate_nonzero]
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['order', 'product']

