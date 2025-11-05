from django.db import models
from .category import Category

from django.contrib.auth.models import User


class Game(models.Model):
    """game model"""

    title = models.CharField(max_length=150)
    description = models.CharField(max_length=300)
    designer = models.CharField(max_length=150)
    year_released = models.CharField(max_length=150)
    number_of_players = models.IntegerField()
    estimated_time_to_play = models.IntegerField()
    age_recommendation = models.IntegerField()
    categories = models.ManyToManyField(Category)
    player_games = models.ManyToManyField(User, blank=True)
    ratings = models.ManyToManyField(
        User, through="Rating", related_name="ratings", blank=True
    )
    images = models.ManyToManyField(
        User, through="GameImage", related_name="images", blank=True
    )
    reviews = models.ManyToManyField(
        User, through="Review", related_name="reviews", blank=True
    )

    def __str__(self):
        return self.title
