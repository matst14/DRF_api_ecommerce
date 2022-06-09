from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api.models import *
import requests

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer de User
    """
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer de Group
    """
    class Meta:
        model = Group
        fields = ['url', 'name']


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer de Order
    """
    total = serializers.SerializerMethodField('get_total')  
    total_usd = serializers.SerializerMethodField('get_usd_total')

    class Meta:
        model = Order
        fields = ['id', 'date_time', 'total', 'total_usd']

    def get_total(self, obj):
        items = OrderDetail.objects.filter(order=obj.id)
        total = 0
        for item in items:
            total = item.cuantity * item.product.price
        return total

    def get_usd_total(self, obj):
        items = OrderDetail.objects.filter(order=obj.id)
        for item in items:
            total = item.cuantity * item.product.price        

        try:
            response = requests.get(
                'https://www.dolarsi.com/api/api.php?type=valoresprincipales'
            )
            response.raise_for_status()
            jsonResponse = response.json()
            for i in jsonResponse:
                if i["casa"]["nombre"] == "Dolar Blue":
                    cotizacion_str = i["casa"]["venta"]
                    cotizacion = cotizacion_str.replace(",",".")
                    return float(cotizacion) * float(total)
        except:
            print(f"Fetch models from api URL failed")

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer de Product
    """
    class Meta:
        model = Product
        fields = ["id", "name", "price", "stock"]

    def validate(self, data):
        """
        Verifica que el stock no sea menor a cero.
        """
        if data['stock'] < 0:
            raise serializers.ValidationError("El stock no puede ser menor a 0")
        elif data['price'] <= 0:
            raise serializers.ValidationError(
                "El precio no puede ser menor o igual a 0"
            )
        return data


class OrderDetailSerializer(serializers.ModelSerializer):
    """
    Serializer de OrderDetail
    """

    class Meta:
        model = OrderDetail
        fields = ['id', 'order', 'cuantity', 'product']

    def validate(self, data):
        """
        Validaciones de cantidad y stock.
        """
        product = Product.objects.get(id=data['product'].pk)
        if data['cuantity'] <= 0:
            raise serializers.ValidationError(
                "La cantidad no puede ser menor a 1"
            )
        elif data['cuantity'] > product.stock:
            raise serializers.ValidationError(
                "La cantidad ingresada supera el stock del producto: " + \
                    str(product.stock)
            )
        return data
    
    def create(self, validated_data):
        """
        Metodo para descontar stock de una instancia de producto cuando se
        crea una orden.
        """
        producto = Product.objects.get(id=validated_data['product'].pk)
        stock_actualizado = producto.stock - validated_data['cuantity']
        producto.stock = stock_actualizado
        producto.save()
        return OrderDetail.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Metodo para descontar stock de una instancia de producto cuando se
        actualiza una orden.
        """        
        instance.cuantity = validated_data.get('cuantity', instance.cuantity)
        instance.product = validated_data.get('product', instance.product)

        producto = Product.objects.get(id=instance.product.pk)
        cantidad_original = OrderDetail.objects.get(id=instance.pk).cuantity

        stock = cantidad_original - instance.cuantity
        stock_actualizado = producto.stock + stock
        producto.stock = stock_actualizado

        producto.save()
        instance.save()
        return instance