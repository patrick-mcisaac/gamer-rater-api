from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from raterapi.models import Category


class CategoryViewSet(ViewSet):
    def list(self, request):
        categories = Category.objects.all()
        serialized = CategorySerializer(categories, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            pass
        except:
            pass


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name"]
