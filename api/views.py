from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver o editar Usuarios.
    """
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver o editar Grupos.
    """
    permission_classes = [IsAuthenticated]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver o editar Productos.
    """
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver o editar Ordenes.
    """    
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderDetailViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver o editar detalles de ordenes.
    """    
    permission_classes = [IsAuthenticated]
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer

    def destroy(self, request, *args, **kwargs):
        """
        Metodo para descontar stock de una instancia de producto cuando se
        elimina una orden.
        """
        orden = self.get_object()

        producto = Product.objects.get(id=orden.product.pk)
        stock_actualizado = producto.stock + orden.cuantity
        producto.stock = stock_actualizado
        producto.save()

        orden.delete()
        return Response(data='delete success')