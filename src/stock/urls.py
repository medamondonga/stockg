"""
url file of stock app
"""
from django.urls import path
from .mixins import ArticleList

urlpatterns = [
    path("articles/", ArticleList.as_view(), name="list-article"),
]
