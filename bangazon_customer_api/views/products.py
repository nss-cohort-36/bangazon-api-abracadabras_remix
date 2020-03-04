from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazon_customer_api.models import Product
from django.contrib.auth.models import User
from .customers  import CustomerSerializer


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
                  'quantity', 'location', 'image_path', 'customer', 'product_type', )
        depth = 1


class Products(ViewSet):
    """products for bangazon"""

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

    def list(self, request):
        """Handle GET requests to products resource
        Returns:
            Response -- JSON serialized list of products
        """
        # customer_id = request.auth.user.customer.id
        products = Product.objects.all()

        # product_name = self.request.query_params.get('name', None)
        # is_one_customer = self.request.query_params.get('customer', False)
        # if is_one_customer == 'true':
        #     products = products.filter(customer__id=customer_id)

        # if product_name is not None:
        #     products = products.filter(name=product_name)

        serializer = ProductsSerializer(
            products, many=True, context={'request': request})
        return Response(serializer.data)