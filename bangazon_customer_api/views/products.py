from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazon_customer_api.models import Product, Customer
# from django.contrib.auth.models import User
from .customers import CustomerSerializer


class ProductsSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for products
    Arguments:
        serializers
    """

    customer = CustomerSerializer(many=False)

    class Meta:
        model = Product
        url = serializers.HyperlinkedIdentityField(
            view_name='product',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'price', 'description',
                  'quantity', 'location', 'image_path', 'customer', 'product_type', 'created_at')
        depth = 2

# /products/1
class Products(ViewSet):
    """products for bangazon"""


    # Get a Single Item 
    # products/1
    def retrieve(self, request, pk=None):
        """Handle GET requests for single product
        Returns:
            Response -- JSON serialized product instance
        """
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductsSerializer(
                product, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    # handles GET all
    # /products
    def list(self, request):
        """Handle GET requests to products resource
        Returns:
            Response -- JSON serialized list of products
        """
        # customer_id = request.auth.user.customer.id
        products = Product.objects.all()
        products = Product.objects.filter(customer_id=request.auth.user.customer.id)


        # product_name = self.request.query_params.get('name', None)
        # is_one_customer = self.request.query_params.get('customer', False)
        # if is_one_customer == 'true':
        #     products = products.filter(customer__id=customer_id)

        # if product_name is not None:
        #     products = products.filter(name=product_name)

        serializer = ProductsSerializer(products, many=True, context={'request': request})
        producttype = self.request.query_params.get('producttype', None)

        if producttype is not None:
            products = products.filter(product_type__id=producttype)

        serializer = ProductsSerializer(
            products, many=True, context={'request': request})
        return Response(serializer.data)

    # handles POST to make a new product
    # products

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized ParkArea instance
        """

        # print(request.auth.user.customer) This print statement digs down into what each of these words mean
        newproduct = Product()
        newproduct.name = request.data["name"]
        newproduct.price = request.data["price"]
        newproduct.description = request.data["description"]
        newproduct.quantity = request.data["quantity"]
        newproduct.location = request.data["location"]
        newproduct.image_path = request.data["image_path"]
        newproduct.created_at = request.data["created_at"]
        # below: we shouldn't send the customer id for security reasons. send as request.auth.user.customer.id - this is your token that represents the user youare logged in as.
        newproduct.customer_id = request.auth.user.customer.id
        newproduct.product_type_id = request.data["product_type_id"]
        newproduct.save()

        serializer = ProductsSerializer(newproduct, context={'request': request})
        # here you are instantiating the  serializer- you are making an instance of a product. you are also making the serializer available within in the scope of the class
        return Response(serializer.data)
        # Response contains data as a property on serializer, which contains the serialized queryset

      # handles PUT to edit

    def update(self, request, pk=None):
        """Handle PUT requests for a product

        Returns:
            Response -- Empty body with 204 status code
        """
        product = Product.objects.get(pk=pk)
        product.name = request.data["name"]
        product.price = request.data["price"]
        product.description = request.data["description"]
        product.quantity = request.data["quantity"]
        product.location = request.data["location"]
        product.image_path = request.data["image_path"]
        product.created_at = request.data["created_at"]
        product.customer_id = request.data["customer_id"]
        product.product_type_id = request.data["product_type_id"]
        product.save()

        serializer = ProductsSerializer(product, context={'request': request})
        return Response(serializer.data)


    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single product

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            product = Product.objects.get(pk=pk)
            product.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        