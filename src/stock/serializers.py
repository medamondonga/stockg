"""
The serializers file of stock app
"""
from decimal import Decimal
from django.conf import settings
from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import (Article, Boutique, PointDeVente,
                     Client, Categorie, Vente, VenteItem,
                     Depense)
User = settings.AUTH_USER_MODEL
#base serializers
class ArticleListSerializer(serializers.ModelSerializer):
    categorie = serializers.CharField(source='categorie.nom_categorie', read_only=True)
    point_de_vente = serializers.CharField(source='point_de_vente.nom_point_de_vente', read_only=True)
    class Meta:
        model = Article
        fields = "__all__"

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # Ajoute les tailles disponibles selon la catégorie liée
        rep['tailles_possibles'] = instance.categorie.get_taille() if instance.categorie else []
        return rep

    def validate(self, attrs):
        categorie = attrs.get('categorie')
        taille = attrs.get('taille')

        if categorie:
            tailles_valides = categorie.get_taille()
            if isinstance(tailles_valides, list) and taille not in tailles_valides:
                raise serializers.ValidationError({
                    'taille': f"La taille '{taille}' n'est pas valide pour la catégorie '{categorie.nom_categorie}'"
                })
        return attrs

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

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"

class VenteItemSerializer(serializers.ModelSerializer):
    article = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all())
    class Meta:
        model = VenteItem
        fields = [
            'article',
            'quantite',
            'prix_unitaire_recu',
            'remise',
            'perte',
        ]
class VenteItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = VenteItem
        fields = "__all__"

class VenteSerializer(serializers.ModelSerializer):
    articles = VenteItemSerializer(many=True, source="vente_items")

    class Meta:
        model = Vente
        fields = [
            'id',
            'client',
            'vendeur',
            'point_de_vente',
            'date_vente',
            'prix_total_vente',
            'articles'
        ]
        read_only_fields = ['id', 'date_vente', 'prix_total_vente']

    def create(self, validated_data):
        articles_data = validated_data.pop("vente_items")
        vente = Vente.objects.create(**validated_data)
        total_vente = Decimal("0.00")

        for item_data in articles_data:
            quantite = int(item_data['quantite'])

            try:
                prix_unitaire = Decimal(str(item_data['prix_unitaire_recu']))
                remise = Decimal(str(item_data.get('remise', 0)))
            except (InvalidOperation, ValueError):
                raise serializers.ValidationError("Prix ou remise invalide.")

            article = item_data['article']

            try:
                prix_achat = Decimal(str(article.prix_achat_unitaire))
            except (InvalidOperation, ValueError, AttributeError):
                raise serializers.ValidationError("Prix d'achat de l'article invalide.")

            perte_calculee = prix_unitaire - prix_achat
            total = (prix_unitaire * quantite) - remise
            total_vente += total

            VenteItem.objects.create(
                vente=vente,
                article=article,
                quantite=quantite,
                prix_unitaire_recu=prix_unitaire,
                remise=remise,
                perte=perte_calculee
            )

        vente.prix_total_vente = total_vente
        vente.save()
        return vente
    
class VenteListSerializer(serializers.ModelSerializer):
    client = serializers.CharField(source='client.nom_client', read_only=True)
    class Meta:
        model = Vente
        fields = "__all__"


class DepensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Depense
        fields = "__all__"

 