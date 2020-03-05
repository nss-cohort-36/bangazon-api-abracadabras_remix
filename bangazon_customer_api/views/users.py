from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from django.http import HttpResponseServerError
from rest_framework.response import Response


class UsersSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for User types

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = Users
        url = serializers.HyperlinkedIdentityField(
            view_name='users',
            lookup_field='id'
        )
        fields = ('id', 'name')

class Users(ViewSet):
    """Users for bangazon"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single user
        Returns:
            Response -- JSON serialized user instance
        """
        try:
            user = User.objects.get(pk=pk)
            serializer = UsersSerializer(
                user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)