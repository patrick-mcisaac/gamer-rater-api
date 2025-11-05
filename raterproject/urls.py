from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from raterapi.views import register_user, login_user, GameViewSet, CategoryViewSet


router = routers.DefaultRouter(trailing_slash=False)
router.register(r"games", GameViewSet, "game")
router.register(r"categories", CategoryViewSet, "category")

urlpatterns = [
    path("", include(router.urls)),
    path("register", register_user),
    path("login", login_user),
    path("admin/", admin.site.urls),
]
