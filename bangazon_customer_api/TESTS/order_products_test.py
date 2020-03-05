import json
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from bagazon_customer_api.models import OrderProduct


class TestOrderProduct(TestCase):

        def setUp(self):
            self.username = 'testuser'
            self.password = 'foobar'
            self.user = User.objects.create_user(username=self.username, password=self.password)
            self.token = Token.objects.create(user=self.user)

        def test_post_order_product(self):
            new_orderproduct = {
                " new_order_id": 1,
                "new_product_id": 1
            }        

        response = self.client.post(
            reverse('orderproduct'), new_orderproduct, HTTP_AUTHORIZATION='Token ' + str(self.token)
          )

        self.assertEqual(response.status_code, 200)
        # self.assertEqual(OrderProduct.objects.count(), 1)
        # self.assertEqual(OrderProduct.objects.get().new_order_id, 1)