from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazon_customer_api.models import Order, OrderProduct, Customer
from .customers import CustomerSerializer

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for orders
    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    
    customer = CustomerSerializer()
    
    class Meta:
        model = Order
        #makes it click
        url = serializers.HyperlinkedIdentityField(
            view_name="order",
            lookup_field='id'
        )
        fields = ('id', 'created_at', 'customer', 'payment_type_id', 'product')
        
        depth = 2
        
class Orders(ViewSet):
    """Orders for Bangazon API"""
    
    #Handles a post request allowing creation with http request
    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized Order instance
        """
        new_order = Order()

        # uncomment this line when AUTH is ready
        new_order.customer_id = request.auth.user.customer.id
        # use this line UTNIL AUTH is ready
        # new_order.customer_id = request.data["customer_id"]
        
        new_order.save()

        serializer = OrderSerializer(
            new_order,
            context={'request': request}
            )

        return Response(serializer.data)

    
    # Get a Single Item 
    def retrieve(self, request, pk=None):
        """Handle GET requests for a single order.
        Fetch call to get one order by order id:
            http://localhost:8000/orders/${id}
        Returns:
            Response -- JSON serialized Order instance
        """
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    # handles GET all, GET by CUSTOMER, and GET by OPEN ORDERS
    def list(self, request):
        """Handle GET requests to orders resource
        Fetch call to get all orders in the database:
            http://localhost:8000/orders
        Fetch call to get all OPEN orders in the database:
            http://localhost:8000/orders/?open=true
        Fetch call to get all orders for the logged in customer:
            http://localhost:8000/orders/?customer=true
        Fetch call to get all OPEN orders for the logged in customer:
            http://localhost:8000/orders/?customer=true&open=true
        Returns:
            Response -- JSON serialized list of orders
        """
        # list of order instances
        orders = Order.objects.all()
        customer_id = request.auth.user.customer.id

        # filter by the logged in customer
        is_one_customer = self.request.query_params.get('customer', False)
        if is_one_customer == 'true':
            orders = orders.filter(customer__id=customer_id)

        # filter by open orders
        is_open = self.request.query_params.get('open', False)
        if is_open == 'true':
            orders = orders.filter(payment_type__id=None)
            
        # takes orders and converts to JSON
        serializer = OrderSerializer(
            orders,
            many=True,
            context={'request': request}
        )
        # Return the JSON
        return Response(serializer.data)


    # handles PUT
    def update(self, request, pk=None):
        """Handle PUT requests for an order
        Returns:
            Response -- Empty body with 204 status code
        """
        order = Order.objects.get(pk=pk)
        order.created_at = request.data["created_at"]
        order.customer_id = request.data["customer_id"]
        order.payment_type_id = request.data["payment_type_id"]
        order.product = request.data["product_id"]
        order.save()

        serializer = OrderSerializer(
            order,
            context={'request': request}
            )

        return Response(serializer.data)


    # handles DELETE
    def destroy(self, request, pk=None):
        """Handles DELETE requests for a single park area
        Returns:
            Response -- 204, 404, or 500 status code
        """
        try:
            order = Order.objects.get(pk=pk)
            order.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]},
            status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.arg[0]},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)