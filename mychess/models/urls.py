from django.urls import path
from models.api import myclassView

urlpatterns = [
    path(r'myclassView/', myclassView.as_view(), name='myclassView'),
]
