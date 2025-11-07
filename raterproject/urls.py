from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from raterapi.views import (
    register_user,
    login_user,
    GameViewSet,
    CategoryViewSet,
    ReviewViewSet,
    RatingViewSet,
    GameImageViewSet,
)


router = routers.DefaultRouter(trailing_slash=False)
router.register(r"games", GameViewSet, "game")
router.register(r"categories", CategoryViewSet, "category")
router.register(r"reviews", ReviewViewSet, "review")
router.register(r"ratings", RatingViewSet, "rating")
router.register(r"game_images", GameImageViewSet, "game_image")

urlpatterns = [
    path("", include(router.urls)),
    path("register", register_user),
    path("login", login_user),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
