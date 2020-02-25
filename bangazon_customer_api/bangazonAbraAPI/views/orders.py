from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonAPI.models import Order, PaymentType, Customer

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    """
    JSON serializer for Orders.py
    
    Feeding in Args:
        serializers
        
    This is a Jeremiah Bell Disaster
    """
    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name = 'order'
            lookup_field = 'id'
        )
        
        fields = ('id',)
    