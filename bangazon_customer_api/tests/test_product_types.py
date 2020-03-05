# THIS IS A FAKE DATABASE that is created and destroyed for every single database! This is what allows us to work with this without crossing streams of databases.

from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.test import TestCase
from django.urls import reverse
from bangazon_customer_api.models import ProductType, Customer

print("test file loads-----------------")


class TestProductType(TestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'foobar'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.customer = Customer.objects.create(
        user=self.user)
        self.token = Token.objects.create(user=self.user)

    def test_post_producttype(self):
        new_producttype = {
            "name": "widgets"
        }

        # use client(client is a specific method not client side) to send the request and store the response
        response = self.client.post(
            reverse('producttype-list'), new_producttype, HTTP_AUTHORIZATION='Token ' + str(self.token)
        )
        
        # 200 get for a success message
        self.assertEqual(response.status_code, 200)
        
        # Query the table to see if there is in fact one instance of PaymentType in it.
        self.assertEqual(ProductType.objects.count(), 1)
        
        # see if it is the one we just addded ensuring the data is passing correctly and accurately
        self.assertEqual(ProductType.objects.get().name, 'widgets')

    def test_get_producttype(self):
        new_producttype = ProductType.objects.create(
          name="widgets r us",
        )

        # Now we can grab all the area (meaning the one we just created) from the db
        response = self.client.get(reverse('producttype-list'))

        # Check that the response is 200 OK.
        # This is checking for the GET request result, not the POST. We already checked that POST works in the previous test!
        self.assertEqual(response.status_code, 200)

        # response.data is the python serialised data used to render the JSON, while response.content is the JSON itself.
        # Are we responding with the data we asked for? There's just one parkarea in our dummy db, so it should contain a list with one instance in it
        self.assertEqual(len(response.data), 1)

        # test the contents of the data before it's serialized into JSON
        self.assertEqual(response.data[0]["name"], "widgets r us")

        # Finally, test the actual rendered content as the client would receive it.
        # .encode converts from unicode to utf-8. Don't get hung up on this. It's just how we can compare apples to apples
        self.assertIn(new_producttype.name.encode(), response.content)

if __name__ == '__main__':
    unittest.main()
