from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Invitation
from stock.models import PointDeVente


class AcceptInvitation(APIView):
    def patch(self, request, id_invitation):
        invitation = get_object_or_404(Invitation, id=id_invitation)
        point_de_vente = invitation.point_de_vente
        user = invitation.email_invite
        token = invitation.token

        if invitation.is_valid(token):
            invitation.accepted()
            point_de_vente.definir_vendeur(user)
            return Response({"message": "Ok"})
        
        return Response({"message": "erreur"})



