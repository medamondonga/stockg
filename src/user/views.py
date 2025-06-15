from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Offre, Abonnement
from .serializers import AbonnementSerializer
from django.utils.timezone import now
from rest_framework.views import APIView

class SouscrireAbonnementView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        offre_id = request.data.get("offre_id")
        try:
            offre = Offre.objects.get(id=offre_id)
        except Offre.DoesNotExist:
            return Response({"error": "Offre non trouvée."}, status=status.HTTP_404_NOT_FOUND)

        # Vérifie s'il y a déjà un abonnement actif
        abonnement_existant = Abonnement.objects.filter(user=request.user, statut="active").first()
        if abonnement_existant:
            return Response({"error": "Vous avez déjà un abonnement actif."}, status=status.HTTP_400_BAD_REQUEST)

        abonnement = Abonnement.objects.create(
            user=request.user,
            offre=offre,
            statut="active",
            date_debut=now()
        )
        serializer = AbonnementSerializer(abonnement)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
