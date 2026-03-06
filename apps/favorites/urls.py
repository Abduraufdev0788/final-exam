from django.urls import path
from .views import FavoriteViews, FavoriteDelete

urlpatterns = [
    path("favorites/", FavoriteViews.as_view(), name="favorites"),
    path("favorites/<int:pk>", FavoriteViews.as_view(), name="favorites"),
]
