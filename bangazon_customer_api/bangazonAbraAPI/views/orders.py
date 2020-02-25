from django.http import HttpResponseServerError
from bangazonAPI.models import Order, PaymentType, Customer
from rest_framework.viewsets import ViewSet
import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    """
    JSON serializer for Orders.py
    
    Feeding in Args for serializers
        
    This is a Jeremiah Bell/Matthew Scott Blagg Disaster
    """
    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name = 'order'
            lookup_field = 'id'
        )
        
        fields = ('url', 'id', 'products' 'created_at', 'payment_type')

class Order(ViewSet):

    def orderCreate (self, request):
        """order instances returned and posts"""
    
        neworder = Order()
        neworder.customer_id = request.auth.user.customer.id
        neworder.payment_type_id = request.data["payment_type_id"]
        neworder.prodcuts= request.data["products"]
        neworder.created_at = requested.data["created_at"]
        neworder.save()
        serializer = OrderSerializer(neworder, context = {"request": request})
        return Response(serializer.data)

    def orderRetrieve(self, request, pk = None):
        """single order request"""

        try: 
            order = Order.objects.get(pk = pk)
            serializer = OrderSerializer(order, context = {"request": request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def orderList(self, request):
        """list of orders"""

        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many = True, context = {"request": request})
        return Response(serializer.data)

    def orderUpdate(self, request, pk = None):
        """Put for orders"""

        order = Order()
        order.customer_id = request.auth.user.customer.id
        order.payment_type = request.data["payment_type"]
        order.products = request.data["products"]
        order.created_at = request.data["created_at"]
        order.save()
        return Response({}, status = status.HTTP_204_NO_CONTENT)

    def orderDestroy(self, request, pk = None):
        """order delete"""

        try: 
            Order = Order.objects.get(pk = pk)
            Order.delete()
            return Response({}, status = status.HTTP_204_NO_CONTENT)

        except Order.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status = status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({"message": ex.args[0]}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
