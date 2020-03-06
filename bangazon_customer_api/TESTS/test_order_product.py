from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.test import TestCase
from django.urls import reverse
from bangazon_customer_api.models import OrderProduct, Customer, Product, Order, ProductType


print("test file loads-----------------")


class TestOrderProduct(TestCase):

        def setUp(self):
            self.username = 'testuser'
            self.password = 'foobar'
            self.user = User.objects.create_user(username=self.username, password=self.password)
            self.customer = Customer.objects.create(
            user=self.user)
            self.token = Token.objects.create(user=self.user)
            self.name = "Food"
            self.product_type_id = ProductType.objects.create(name=self.name)
            self.price = 2.99
            self.description = "gallon"
            self.quantity = 1
            self.location = "Nashville"
            self.name = "Water"
            self.image_path = "spings"
            self.created_at = "01/12/2020"
            self.customer_id = 1
            self.product_type_id = 1
            self.product_id = Product.objects.create(name=self.name, price=self.price, description=self.description, 
            quantity=self.quantity, product_type_id=self.product_type_id, location=self.location, image_path=self.image_path, created_at=self.created_at, customer_id=self.customer_id)
            self.paymenttype = 1
            self.created_at = "03/12/1995"
            self.order_id = Order.objects.create(customer_id=self.customer_id, created_at=self.created_at)

        def test_post_order_product(self):
            new_orderproduct = {
                "order_id": 1,
                "product_id": 1
            } 

                  

            response = self.client.post(
                reverse('orderproduct-list'), new_orderproduct, HTTP_AUTHORIZATION='Token ' + str(self.token)
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(OrderProduct.objects.count(), 1)
            self.assertEqual(OrderProduct.objects.get().order_id, 1)


        def test_get_order_product(self):
            new_orderproduct = OrderProduct.objects.create(
                order_id=1,
                product_id=1,
            )

            response = self.client.get(reverse('orderproduct-list'))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]["order_id"], 1)
            # self.assertIn( new_orderproduct.order_id, response.content)

if __name__ == '__main__':
    unittest.main()       