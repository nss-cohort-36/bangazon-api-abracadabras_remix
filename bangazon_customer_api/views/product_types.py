from rest_framework.viewsets import ViewSet
from bangazon_customer_api.models import ProductType
from rest_framework import status
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
        # product_types = ProductType.objects.filter(product_type_id=)

        serializer = ProductTypeSerializer(
            product_types,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        try:
            product_type = ProductType.objects.get(pk=pk)
            serializer = ProductTypeSerializer(
                product_type,
                context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized Order instance
        """
        new_type = ProductType()
        new_type.name = request.data["name"]

        new_type.save()

        serializer = ProductTypeSerializer(new_type, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for a producttype
        Returns:
            Response -- Empty body with 204 status code
        """
        type = ProductType.objects.get(pk=pk)
        type.name = request.data["name"]
        type.save()

        serializer = ProductTypeSerializer(
            type,
            context={'request': request}
            )
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handle DELETE requests to product type
        Return:
        Response -- JSON serialized detail of deleted product type
        """
        try:
            producttype = ProductType.objects.get(pk=pk)
            producttype.delete()
        
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except ProductType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


