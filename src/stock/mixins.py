"""
The mixins file of stock app
"""
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView
from .models import Article
from .serializers import ArticleSerializer

class ArticleList(ListModelMixin, GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request, *args,**kwargs):
        return self.list(request, *args, **kwargs)