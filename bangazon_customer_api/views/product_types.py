from rest_framework.viewsets import ViewSet
from bangazon_customer_api.models import ProductType
from rest_framework import serializers
from rest_framework.response import Response
from django.http import HttpResponseServerError

class ProductTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for product types

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = ProductType
        url = serializers.HyperlinkedIdentityField(
            view_name='producttype',
            lookup_field='id'
        )
        fields = ('id', 'name')

class ProductTypes(ViewSet):
    def list(self, request):
        
        """Handle GET requests to park attractions resource

        Returns:
            Response -- JSON serialized list of park attractions
        """
        
        product_types = ProductType.objects.all()
        serializer = ProductTypeSerializer(
            product_types,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
        
    def retrieve(self, request, pk=None):
        """Handle GET requests to product types resource for a single product type

        Returns:
            Response -- JSON serialized list of park areas
        """
        try:
            product_type = ProductType.objects.get(pk=pk)
            serializer = ProductTypeSerializer(
                product_type,
                context={'request': request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
