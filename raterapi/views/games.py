from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from raterapi.models import Game


class GameViewSet(ViewSet):

    def list(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = [
            "id",
            "title",
            "description",
            "designer",
            "year_released",
            "number_of_players",
            "estimated_time_to_play",
            "age_recommendation",
            "categories",
            "player_games",
        ]
