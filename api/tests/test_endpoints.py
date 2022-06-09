# Django
from django.test import TestCase
from django.contrib.auth.models import User
from ..models import *

# Python
import json

# Django Rest Framework
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class UserEndPointsTestCase(TestCase):
    """
    Valida endpoints de User
    """

    def setUp(self):
        user = User.objects.create_user(
            username='usuario', password='muysegura'
        )
        client = APIClient()
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        return client


class ProductEndPointsTestCase(TestCase):
    """
    Valida endpoints de Products
    """

    def test_create_product_success(self):
        """
        Verifica la creación de un producto de manera exitosa.
        """
        user = User.objects.create_user(
            username='usuario', password='muysegura'
        )
        client = APIClient()
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        test_product = {
            'id': 1,
            'name': 'producto 1',
            'price': 99.99,
            'stock': 200,
        }

        response = client.post(
            '/products/', 
            test_product,
            format='json'
        )

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', result)
        self.assertIn('name', result)
        self.assertIn('price', result)
        self.assertIn('stock', result)

        if 'pk' in result:
            del result['pk']

        self.assertEqual(result, test_product)

    def test_create_product_error(self):
        """
        Verifica que no se pueda crear un producto si el precio o el stock
        tienen valores negativos.
        """

        user = User.objects.create_user(
            username='usuario', password='muysegura'
        )
        client = APIClient()
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        test_product = {
            'id': 1,
            'name': 'producto 1',
            'price': -99.99,
            'stock': -200,
        }

        response = client.post(
            '/products/', 
            test_product,
            format='json'
        )

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)


class OrderDetailEndPointsTestCase(TestCase):
    """
    Valida endpoints de OrderDetail
    """

    def test_create_order_detail_success(self):
        """
        Verifica la creación de un detalle de orden de manera exitosa.
        """
        user = User.objects.create_user(
            username='usuario', password='muysegura'
        )
        client = APIClient()
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        order = Order.objects.create(
            date_time='2022-06-01T15:39:00'
        )

        product = Product.objects.create(
            name= 'producto 1',
            price= 99.99,
            stock= 200,
        )

        test_order_detail = {
            'id': 1,
            'order': order.pk,
            'cuantity': 1,
            'product': product.pk,
        }

        response = client.post(
            '/order-detail/', 
            test_order_detail,
            format='json'
        )

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', result)
        self.assertIn('order', result)
        self.assertIn('cuantity', result)
        self.assertIn('product', result)

        if 'pk' in result:
            del result['pk']

        self.assertEqual(result, test_order_detail)

    def test_create_order_detail_error(self):
        """
        Verifica que no se pueda crear un detalle de orden si la cantidad supera
        al stock del producto.
        """

        user = User.objects.create_user(
            username='usuario', password='muysegura'
        )
        client = APIClient()
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        order = Order.objects.create(
            date_time='2022-06-01T15:39:00'
        )

        product = Product.objects.create(
            name= 'producto 1',
            price= 99.99,
            stock= 200,
        )

        test_order_detail = {
            'id': 1,
            'order': order.pk,
            'cuantity': 201,
            'product': product.pk,
        }

        response = client.post(
            '/order-detail/', 
            test_order_detail,
            format='json'
        )

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
