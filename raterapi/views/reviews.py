from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from raterapi.models import Review, Game
from django.contrib.auth.models import User


class ReviewViewSet(ViewSet):
    def list(self, request):
        reviews = Review.objects.all()
        game = request.query_params.get("game", None)

        if game is not None and game.isdigit():
            reviews = reviews.filter(game=int(game))

        serialized = ReviewSerializer(reviews, many=True)

        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        pass

    def create(self, request):
        try:
            game = Game.objects.get(pk=request.data.get("game"))
            user = request.user
            review = Review.objects.create(
                review=request.data.get("review"), game=game, user=user
            )
            serialized = ReviewSerializer(review, many=False)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        except Exception:
            pass


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ["id", "review", "game", "user"]
