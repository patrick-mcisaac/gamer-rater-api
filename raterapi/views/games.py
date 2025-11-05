from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from raterapi.models import Game, Category


class GameViewSet(ViewSet):

    def list(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        try:
            category = Category.objects.get(pk=request.data.get("categories"))

            game = Game.objects.create(
                title=request.data.get("title"),
                description=request.data.get("description"),
                designer=request.data.get("designer"),
                year_released=request.data.get("year_released"),
                number_of_players=request.data.get("number_of_players"),
                estimated_time_to_play=request.data.get("estimated_time_to_play"),
                age_recommendation=request.data.get("age_recommendation"),
            )

            game.categories.add(category)
            serialized = GameSerializer(game, many=False, context={"request": request})
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)


class GameCategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name"]


class GameSerializer(serializers.ModelSerializer):

    categories = GameCategoriesSerializer(many=True)

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
