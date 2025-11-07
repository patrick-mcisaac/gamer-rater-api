from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from raterapi.models import Game, Category
from django.contrib.auth.models import User
from django.db.models import Q


class GameViewSet(ViewSet):

    def list(self, request):
        search_text = self.request.query_params.get("q", None)
        sort_term = self.request.query_params.get("orderby", None)

        if search_text is not None:
            games = Game.objects.filter(
                Q(title__contains=search_text)
                | Q(description__contains=search_text)
                | Q(designer__contains=search_text)
            )
        else:
            games = Game.objects.all()

        if sort_term is not None:
            if sort_term == "time":
                games = games.order_by("estimated_time_to_play")
            elif sort_term == "designer":
                games = games.order_by("designer")
            elif sort_term == "year":
                games = games.order_by("year_released")
        serializer = GameSerializer(games, many=True, context={"request": request})
        return Response(serializer.data, status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, many=False, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        try:
            category = Category.objects.get(pk=request.data.get("categories"))
            user = request.user

            game = Game.objects.create(
                title=request.data.get("title"),
                description=request.data.get("description"),
                designer=request.data.get("designer"),
                year_released=request.data.get("year_released"),
                number_of_players=request.data.get("number_of_players"),
                estimated_time_to_play=request.data.get("estimated_time_to_play"),
                age_recommendation=request.data.get("age_recommendation"),
                user=user,
            )

            game.categories.add(category)
            serialized = GameSerializer(game, many=False, context={"request": request})
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)

            serialized = UpdateGameSerializer(game, data=request.data)

            if serialized.is_valid():
                serialized.save()

                serialized = GameSerializer(
                    game, many=False, context={"request": request}
                )
                return Response(serialized.data, status=status.HTTP_200_OK)
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        except Game.DoesNotExist as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND)


class GameCategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name"]


class GameSerializer(serializers.ModelSerializer):

    is_creator = serializers.SerializerMethodField()
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
            "user",
            "is_creator",
            "average_rating",
        ]

    def get_is_creator(self, obj):
        return self.context["request"].user == obj.user


class UpdateGameSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=False
    )

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
        ]

    def update(self, instance, validated_data):
        categories_data = validated_data.pop("categories", None)
        for key, value in validated_data.items():
            setattr(instance, key, value)

        if categories_data is not None:

            instance.categories.set(categories_data)
        instance.save()
        return instance

    def validate_categories(self, value):
        if not isinstance(value, list):
            return [value]
        return value


# class GameUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields
