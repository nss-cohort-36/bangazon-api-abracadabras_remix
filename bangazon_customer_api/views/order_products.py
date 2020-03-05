from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazon_customer_api.models import Product, Order, Customer, OrderProduct



class OrderProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for order_product

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = OrderProduct
        url = serializers.HyperlinkedIdentityField(
            view_name='OrderProducts',
            lookup_field='id'
        )
        fields = ('id', 'product_id', 'order_id')
        depth = 2


class OrderProducts(ViewSet):


    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized Order Product instance
        """
        new_order_product = OrderProduct()
        new_order_product.order_id = request.data["order_id"]
        new_order_product.product_id = request.data["product_id"]
        new_order_product.save()

        serializer = OrderProductSerializer(
            new_order_product, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
            """Handle GET requests for order_product

            Returns:
                Response -- JSON serialized order_product instance
            """

            try:
                order_product = OrderProduct.objects.get(pk=pk)
                serializer = OrderProductSerializer(order_product, context={'request': request})
                return Response(serializer.data)
            except Exception as ex:
                return HttpResponseServerError(ex)


    def list(self, request):
        """Handle GET requests to order_products 
        Returns:
            Response -- JSON serialized list of order_products
        """
        order_product = OrderProduct.objects.all()

        order_id = self.request.query_params.get('order', None)
        if order_id is not None:
            order_product = order_product.filter(order__id=order_id)

        serializer = OrderProductSerializer(
            order_product, many=True, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a order_product
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            order_product = OrderProduct.objects.get(pk=pk)
            order_product.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



