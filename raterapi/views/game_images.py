from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status, serializers
from raterapi.models import GameImage, Game
import uuid
import base64
from django.core.files.base import ContentFile


class GameImageViewSet(ViewSet):
    def create(self, request):
        try:
            image = GameImage()

            format, imgstr = request.data["game_image"].split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(
                base64.b64decode(imgstr),
                name=f'{request.data["game_id"]}-{uuid.uuid4()}.{ext}',
            )

            image.image = data

            game = Game.objects.get(pk=request.data.get("game_id"))

            user = request.user

            image.game = game
            image.user = user

            image.save()
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class GameImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = GameImage
        fields = ["image", "game"]
