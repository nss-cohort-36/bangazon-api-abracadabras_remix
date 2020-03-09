from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazon_customer_api.models import PaymentType, Customer

# Required Imports for functionality Above ^ allows use of framework Viewset, Response, Serializers(what changes data type) PaymentType and Customer are Models we created for blueprints later. JB- Comment

# Establishing Class for Payment Type Serializer. Converts Payment Type Data for consumption as JSON.

class PaymentTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for payment types

    Arguments:
        serializers.HyperlinkedModelSerializer

    Author: Jeremiah Bell
    """

    class Meta:
        model = PaymentType
        url = serializers.HyperlinkedIdentityField(
            view_name='paymenttype',
            lookup_field='id'
        )
        fields = ('id', 'merchant_name', 'acct_number', 'expiration_date', 'customer_id', 'created_at')
        # depth is only necessary with foreign keys.
        depth = 2

# Handling GET requests for Data of one payment type
class PaymentTypes(ViewSet):
        def retrieve(self, request, pk=None):
            """This is supposed to Handle GET requests for one payment type

            Return:
                This returns a json serialized payment type instance
            Author: JBell
            """

            try:
                payment_type = PaymentType.objects.get(pk=pk)
                serializer = PaymentTypeSerializer(payment_type,
                context = {'request': request})
                return Response(serializer.data)
            except Exception as ex:
                return HttpResponseServerError(ex)

        def list(self, request):
            """Handle Gets for payment type

            Return:
                This returns json serialized(jsonified) list of payment types
            """
            
            
            payment_types = PaymentType.objects.all()
            payment_types = PaymentType.objects.filter(customer_id=request.auth.user.customer.id)
            
            # setting variable customer locally equal to self(paymentTypeClassObject) and checking to see if there is a customer in the request.
            # customer = self.request.query_params.get('customer', None) 

            # if customer is not None:
            #     payment_types = payment_types.filter(customer_id=customer)

            serializer = PaymentTypeSerializer(payment_types, many = True, context={'request': request})

            return Response(serializer.data)
        # this is how you handle delete with djanog. Destroy is the word or key for this method
        def destroy(self, request, pk=None):
            """Handle DELETE requests to payment type

            Return:
            Response -- JSON serialized detail of deleted payment type
        """
            try:
                paymenttype = PaymentType.objects.get(pk=pk)
                paymenttype.delete()

                return Response({}, status=status.HTTP_204_NO_CONTENT)

            except PaymentType.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

            except Exception as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# This should handle the update or edit request. -JB
        def update(self, request, pk=None):
            """Handle PUT requests for an individual payment type item
            Returns:
            Response -- Empty body with 204 status code
            """
            paymenttype = PaymentType.objects.get(pk=pk)
            paymenttype.merchant_name = request.data["merchant_name"]
            paymenttype.acct_number = request.data["acct_number"]
            paymenttype.expiration_date = request.data["expiration_date"]
            paymenttype.customer_id = request.auth.user.customer.id

            paymenttype.save()

            serializer = PaymentTypeSerializer(paymenttype, context={'request': request})

            return Response(serializer.data)

    # Handles the creation of an object
        def create(self, request):
            new_paymenttype = PaymentType()
            new_paymenttype.merchant_name = request.data["merchant_name"]
            new_paymenttype.acct_number = request.data["acct_number"]
            new_paymenttype.expiration_date = request.data["expiration_date"]
            new_paymenttype.customer_id = request.auth.user.customer.id

            new_paymenttype.save()

            serializer = PaymentTypeSerializer(new_paymenttype, context={'request': request})

            return Response(serializer.data)

