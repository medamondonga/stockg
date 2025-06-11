"""
The serializers file of stock app
"""
from decimal import Decimal, InvalidOperation
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
        read_only_fields = ["total"]


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
        ventes_data = validated_data.pop("vente_items")
        total_vente = 0

        # Vérifie le stock avant de créer la vente
        for vente_data in ventes_data:
            article = vente_data['article']
            quantite = vente_data['quantite']
            if article.quantite_en_stock < quantite:
                raise serializers.ValidationError(
                    f"Stock insuffisant pour l'article '{article.nom_article}'. "
                    f"Disponible : {article.quantite_en_stock}, demandé : {quantite}."
                )
            total_vente += vente_data['prix_unitaire_recu'] * quantite

        # Crée la vente maintenant que tout est validé
        vente = Vente.objects.create(prix_total_vente=total_vente, **validated_data)

        # Crée les vente_items et met à jour le stock
        for vente_data in ventes_data:
            article = vente_data['article']
            quantite = vente_data['quantite']
            prix_recu = vente_data['prix_unitaire_recu']
            remise = vente_data.get('remise', 0)
            perte = 0

            total_item = prix_recu * quantite
            benefice_item = (prix_recu - article.prix_achat_unitaire) * quantite
            if benefice_item < 0:
                perte = abs(benefice_item)
                benefice_item = 0


            VenteItem.objects.create(
                vente=vente,
                article=article,
                quantite=quantite,
                prix_unitaire_recu=prix_recu,
                remise=remise,
                perte=perte,
                total=total_item,
                benefice=benefice_item
            )

            # Mise à jour du stock
            article.quantite_en_stock -= quantite
            article.save()

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

 