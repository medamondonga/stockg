from rest_framework.generics import ListAPIView
from .models import VenteItem, Article, Depense, Vente, PointDeVente, Boutique
from .serializers import VenteItemDetailSerializer, PointDeVenteSerializer, BoutiqueSerializer
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from rest_framework import serializers, viewsets

from rest_framework.response import Response
from rest_framework.decorators import api_view
from stockg.generic_crud import get_proprio_user


class PointDeVenteViewSet(viewsets.ModelViewSet):
    serializer_class = PointDeVenteSerializer

    def get_queryset(self):
        user = get_proprio_user(self.request.user)
        return PointDeVente.objects.filter(boutique__proprietaire=user)

    def perform_create(self, serializer):
        boutique_id = self.request.data.get("boutique")
        user = get_proprio_user(self.request.user)
        try:
            boutique = Boutique.objects.get(id=boutique_id, proprietaire=user)
            serializer.save(gerant=self.request.user, boutique=boutique)
        except Boutique.DoesNotExist:
            raise serializers.ValidationError("Boutique non trouvée ou accès interdit.")


class BoutiqueViewSet(viewsets.ModelViewSet):
    serializer_class = BoutiqueSerializer

    def get_queryset(self):
        user = get_proprio_user(self.request.user)
        return Boutique.objects.filter(proprietaire=user)

    def perform_create(self, serializer):
        user = get_proprio_user(self.request.user)
        serializer.save(proprietaire=user)


class VenteItemByVenteView(ListAPIView):
    serializer_class = VenteItemDetailSerializer

    def get_queryset(self):
        vente_id = self.request.query_params.get('vente_id')
        user = get_proprio_user(self.request.user)
        if vente_id:
            return VenteItem.objects.filter(vente_id=vente_id, vente__proprietaire=user)
        return VenteItem.objects.none()

    
@api_view(['GET'])
def produits_les_plus_vendus(request):
    user = get_proprio_user(request.user)
    data = (
        VenteItem.objects
        .filter(vente__proprietaire=user)
        .values('article__nom_article')
        .annotate(total_vendus=Sum('quantite'))
        .order_by('-total_vendus')[:8]
    )
    return Response(data)

@api_view(['GET'])
def statistiques_dashboard(request):
    user = get_proprio_user(request.user)
    maintenant = timezone.now().date()
    il_y_a_7_jours = maintenant - timedelta(days=7)

    total_articles = Article.objects.filter(proprietaire=user).aggregate(
        total=Sum('quantite_en_stock'))['total'] or 0

    ventes_7j = Vente.objects.filter(
        date_vente__gte=il_y_a_7_jours,
        proprietaire=user
    ).aggregate(total=Sum('prix_total_vente'))['total'] or 0

    benefice_7j = VenteItem.objects.filter(
        vente__date_vente__gte=il_y_a_7_jours,
        vente__proprietaire=user
    ).aggregate(total=Sum('benefice'))['total'] or 0

    depenses_7j = Depense.objects.filter(
        date_depense__gte=il_y_a_7_jours,
        proprietaire=user
    ).aggregate(total=Sum('montant'))['total'] or 0

    data = {
        'articles': total_articles,
        'ventes': ventes_7j,
        'benefice': benefice_7j,
        'depense': depenses_7j
    }
    return Response(data)
