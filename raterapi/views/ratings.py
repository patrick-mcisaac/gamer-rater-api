from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models import Rating, Game


class RatingViewSet(ViewSet):
    def list(self, request):
        ratings = Rating.objects.all()

        game = request.query_params.get("game", None)
        player = request.query_params.get("user", None)

        if game is not None:
            ratings = ratings.filter(game=game)

        if player is not None and player == "current":
            ratings = ratings.filter(user=request.user)

        serialized = RatingSerializer(ratings, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        pass

    def create(self, request):
        try:
            game = Game.objects.get(pk=request.data.get("game"))
            rating = Rating.objects.create(
                rating=request.data.get("rating"), game=game, user=request.user
            )
            serialized = RatingSerializer(rating, many=False)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        except Exception:
            return Response("", status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            rating = Rating.objects.get(pk=pk)
            serialized = UpdateRatingSerializer(rating, data=request.data)

            if serialized.is_valid():
                serialized.save()

                serialized = RatingSerializer(rating, many=False)
                return Response(serialized.data, status=status.HTTP_200_OK)
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        except Rating.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ["id", "rating", "game", "user"]


class UpdateRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = [
            "rating",
        ]
