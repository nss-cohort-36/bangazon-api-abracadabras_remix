# import dependencies
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazon_customer_api.models import Customer
from django.contrib.auth.models import User

# Serializer
class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for customers

    Arguments:
        base serializer class
    """

    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customer',
            lookup_field='id'
        )
        fields = ('id', 'url', 'user_id')


# Request handler
class Customers(ViewSet):
    """customers for bangazon"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single customer
        Returns:
            Response -- JSON serialized customer instance
        """
        try:
            customer = Customer.objects.get(pk=pk)
            serializer = CustomerSerializer(
                customer, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
        
    def update(self, request, pk=None):
        """Handles Edit/Update Request
        Response is passing error message 204.
        """
        customer = Customer.objects.get(pk=pk)
        user = customer.user
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.email = request.data["email"]
        
        user.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    # Creating a List Element so We can at least see a list of users if we want too, since this is the back end.
    def list(self, request, pk=None):
        """Handle GET request listing of customers endpoint
        Returns:
            Response: List of Customers as JSON
        """
        customers = Customer.objects.all()
        customers = Customer.objects.filter(customer_id=request.auth.user.customer.id)

        
        # if customer is not None:
        #     customers = customers.filter(id=customer)
            
        serializer = CustomerSerializer(customers, many=True, context={'request': request})
        return Response(serializer.data)