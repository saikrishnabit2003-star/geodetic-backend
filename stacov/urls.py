from django.urls import path
from .views import StacovByDateAPIView


urlpatterns = [

    path("stacov/", StacovByDateAPIView.as_view(), name="stacov-by-date"),
]

