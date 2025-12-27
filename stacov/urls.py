from django.urls import path
from .views import StacovByDateAPIView
from .views import ping

urlpatterns = [
    path("ping/", ping),
    path("stacov/", StacovByDateAPIView.as_view(), name="stacov-by-date"),
]

