from rest_framework.viewsets import ViewSet
from bangazon_customer_api.models import ProductType
from rest_framework import serializers
from rest_framework.response import Response

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
        
