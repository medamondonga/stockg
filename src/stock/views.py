from rest_framework.generics import ListAPIView
from .models import VenteItem, Article, Depense, Vente, PointDeVente, Boutique
from .serializers import VenteItemDetailSerializer, PointDeVenteSerializer, BoutiqueSerializer
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from rest_framework import serializers, viewsets

from rest_framework.response import Response
from rest_framework.decorators import api_view


class PointDeVenteViewSet(viewsets.ModelViewSet):
    queryset = PointDeVente.objects.all()
    serializer_class = PointDeVenteSerializer

    def perform_create(self, serializer):
        boutique_id = self.request.data.get("boutique")
        try:
            boutique = Boutique.objects.get(id=boutique_id, proprietaire=self.request.user)
            serializer.save(gerant=self.request.user, boutique=boutique)
        except Boutique.DoesNotExist:
            raise serializers.ValidationError("Boutique non trouvée ou accès interdit.")

class BoutiqueViewSet(viewsets.ModelViewSet):
    queryset = Boutique.objects.all()
    serializer_class = BoutiqueSerializer

    def perform_create(self, serializer):
        serializer.save(proprietaire=self.request.user)








class VenteItemByVenteView(ListAPIView):
    serializer_class = VenteItemDetailSerializer

    def get_queryset(self):
        vente_id = self.request.query_params.get('vente_id')
        if vente_id:
            return VenteItem.objects.filter(vente_id=vente_id)
        return VenteItem.objects.none()
    
@api_view(['GET'])
def produits_les_plus_vendus(request):
    data = (
        VenteItem.objects
        .values('article__nom_article')  # adapte si champ = nom
        .annotate(total_vendus=Sum('quantite'))
        .order_by('-total_vendus')[:8]
    )
    return Response(data)


@api_view(['GET'])
def statistiques_dashboard(request):
    maintenant = timezone.now().date()  # car date_vente est un DateField
    il_y_a_7_jours = maintenant - timedelta(days=7)

    # Articles en stock = total des quantités
    total_articles = Article.objects.aggregate(total=Sum('quantite_en_stock'))['total'] or 0

    # Ventes sur les 7 derniers jours
     # Total des ventes (en argent reçu) sur les 7 derniers jours
    ventes_7j = (
        Vente.objects
        .filter(date_vente__gte=il_y_a_7_jours)
        .aggregate(total=Sum('prix_total_vente'))['total'] or 0)

    # Bénéfice des 7 derniers jours
    benefice_7j = (
        VenteItem.objects
        .filter(vente__date_vente__gte=il_y_a_7_jours)
        .aggregate(total=Sum('benefice'))['total'] or 0
    )

    # Dépenses des 7 derniers jours
    depenses_7j = (
        Depense.objects
        .filter(date_depense__gte=il_y_a_7_jours)
        .aggregate(total=Sum('montant'))['total'] or 0
    )

    data = {
        'articles': total_articles,
        'ventes': ventes_7j,
        'benefice': benefice_7j,
        'depense': depenses_7j
    }
    return Response(data)