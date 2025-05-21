"""
The serializers file of stock app
"""
from rest_framework import serializers
from .models import Article, Boutique, PointDeVente, Client, Categorie

#base serializers
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"

class BoutiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boutique
        fields = "__all__"

class PointDeVenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointDeVente
        fields = "__all__"

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = "__all__"