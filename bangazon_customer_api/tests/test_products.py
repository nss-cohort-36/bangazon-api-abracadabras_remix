# THIS IS A FAKE DATABASE that is created and destroyed for every single database! This is what allows us to work with this without crossing streams of databases.

from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.test import TestCase
from django.urls import reverse
from bangazon_customer_api.models import Product, ProductType, Customer

print("test file loads-----------------")


class TestProduct(TestCase):

    def setUp(self):
        self.name = "Toys"
        self.username = 'testuser'
        self.password = 'foobar'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.customer = Customer.objects.create(user=self.user)
        self.product_type_id = ProductType.objects.create(name=self.name)
        self.token = Token.objects.create(user=self.user)

    def test_post_product(self):
        # Creating an instance of an object for product?
        # I think I need to create an example object to post here based on what is shown in the chapter.
        #    Example object from PaymentType match too instance of fixture so that it will be an actual post, but will not actually show in the database.
        # new_area = {
                #   "name": "Halloween Land",
                #   "theme": "spooky stuff"
                # }
        # set a local variable where new_area is:
    
        new_product = {
        "name": "Tyke Bike",
        "price": 10.00,
        "quantity": 1,
        "description": "A mighty bike for tiny tykes",
        "location": "Nashville",
        "image_path": "./none_pic.jpg",
        "created_at": "2020-02-21 00:00:00",
        "customer_id": 1,
        "product_type_id": 1
      }

        # use client(client is a specific method not client side) to send the request and store the response
        response = self.client.post(
            reverse('product-list'), new_product, HTTP_AUTHORIZATION='Token ' + str(self.token)
        )
        
        # 200 get for a success message
        self.assertEqual(response.status_code, 200)
        
        # Query the table to see if there is in fact one instance of PaymentType in it.
        self.assertEqual(Product.objects.count(), 1)
        
        # see if it is the one we just addded ensuring the data is passing correctly and accurately
        self.assertEqual(Product.objects.get().name, 'Tyke Bike')


    def test_get_product(self):

        #  def test_get_parkareas(self):
        # new_area = ParkArea.objects.create(
        #   name="Coaster Land",
        #   theme="coasters, duh",
        # )

        product = Product.objects.create(
            name = "Tyke Bike",
            price = 10.00,
            quantity = 1,
            description = "A mighty bike for tiny tykes",
            location = "Nashville",
            image_path = "./none_pic.jpg",
            created_at = "2020-02-21 00:00:00",
            customer_id = 1,
            product_type_id = 1
        )


        # use client(client is a specific method not client side)
        # Now we can grab all the area (meaning the one we just created) from the db
        response = self.client.get(
            reverse('product-list'), HTTP_AUTHORIZATION='Token ' + str(self.token)
        ) 
        
        # # Check that the response is 200 OK.
        # # This is checking for the GET request result, not the POST. We already checked that POST works in the previous test!
        self.assertEqual(response.status_code, 200)
        
        # # response.data is the python serialised data used to render the JSON, while response.content is the JSON itself.
        # # Are we responding with the data we asked for? There's just one parkarea in our dummy db, so it should contain a list with one instance in it
        self.assertEqual(len(response.data), 1)

        # test the contents of the data before it's serialized into JSON
        self.assertEqual(response.data[0]["name"], "Tyke Bike")

        # # Finally, test the actual rendered content as the client would receive it.
        # # .encode converts from unicode to utf-8. Don't get hung up on this. It's just how we can compare apples to apples
        self.assertIn(product.name.encode(), response.content)
       
    def test_list_products(self):

        product = Product.objects.create(
            name = "Tyke Bike",
            price = 10.00,
            quantity = 1,
            description = "A mighty bike for tiny tykes",
            location = "Nashville",
            image_path = "./none_pic.jpg",
            created_at = "2020-02-21 00:00:00",
            customer_id = 1,
            product_type_id = 1
        )

        product = Product.objects.create(
            name = "Blue Bike",
            price = 10.00,
            quantity = 1,
            description = "A mighty bike for tiny tykes",
            location = "Nashville",
            image_path = "./none_pic.jpg",
            created_at = "2020-02-21 00:00:00",
            customer_id = 1,
            product_type_id = 1
        )

        # use client(client is a specific method not client side)
        # Now we can grab all the area (meaning the one we just created) from the db
        response = self.client.get(
            reverse('product-list'), HTTP_AUTHORIZATION='Token ' + str(self.token)
        ) 
        
        # # Check that the response is 200 OK.
        # # This is checking for the GET request result, not the POST. We already checked that POST works in the previous test!
        self.assertEqual(response.status_code, 200)
        
        # # response.data is the python serialised data used to render the JSON, while response.content is the JSON itself.
        # # Are we responding with the data we asked for? There's just one parkarea in our dummy db, so it should contain a list with one instance in it
        self.assertEqual(len(response.data), 2)

        # test the contents of the data before it's serialized into JSON
        self.assertEqual(response.data[0]["name"], "Tyke Bike", "Red Shirt" )

        # # Finally, test the actual rendered content as the client would receive it.
        # # .encode converts from unicode to utf-8. Don't get hung up on this. It's just how we can compare apples to apples
        self.assertIn(product.name.encode(), response.content)
              

   
if __name__ == '__main__':
    unittest.main()
