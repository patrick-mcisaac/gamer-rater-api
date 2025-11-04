from django.contrib import admin
from .models import Category, GameImage, Game, Rating, Review


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


class GameImageAdmin(admin.ModelAdmin):
    list_display = ("game", "image")


class RatingAdmin(admin.ModelAdmin):
    list_display = ("game", "rating", "user")


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("game", "user")


# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(GameImage, GameImageAdmin)
admin.site.register(Game)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Review, ReviewAdmin)
