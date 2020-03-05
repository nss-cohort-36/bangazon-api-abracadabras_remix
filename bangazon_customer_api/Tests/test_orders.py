# THIS IS A FAKE DATABASE that is created and destroyed for every single database! This is what allows us to work with this without crossing streams of databases.

from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.test import TestCase
from django.urls import reverse
from bangazon_customer_api.models import PaymentType, Customer, Order

print("test file loads-----------------")


class TestOrders(TestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'foobar'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.customer = Customer.objects.create(
        user=self.user)
        self.token = Token.objects.create(user=self.user)

    def test_post_orders(self):
        # Creating an instance of an object for payment type?
        # I think I need to create an example object to post here based on what is shown in the chapter.
        #    Example object from Order match too instance of fixture so that it will be an actual post, but will not actually show in the database.
        
        new_orders = {
            "customer": "1",
            "payment_type": "3",
            "created_at": "2024-01-01"
        }

        # use client(client is a specific method not client side) to send the request and store the response
        response = self.client.post(
            reverse('order-list'), new_orders, HTTP_AUTHORIZATION='Token ' + str(self.token)
        )
        
        # 200 get for a success message
        self.assertEqual(response.status_code, 200)
        
        # Query the table to see if there is in fact one instance of Order in it.
        self.assertEqual(Order.objects.count(), 1)
        
        # see if it is the one we just addded ensuring the data is passing correctly and accurately
        self.assertEqual(Order.objects.get().payment_type, '3')

if __name__ == '__main__':
    unittest.main()
