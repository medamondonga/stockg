from django.shortcuts import HttpResponse
from .serializers import (EmailTokenObtainPairSerializer, 
                          UserSerializer, AjouterVendeurSerializer,
                          SignupVendeurSerializer, MeSerializer)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import CreateAPIView, DestroyAPIView, GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import VendeurAssociation
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()




class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    serializer = MeSerializer(request.user)
    return Response(serializer.data)

class AjouterVendeurView(CreateAPIView):
    serializer_class = AjouterVendeurSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}

class SupprimerVendeurView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        vendeur_id = self.kwargs.get("vendeur_id")
        association = get_object_or_404(VendeurAssociation, vendeur_id=vendeur_id, proprietaire=request.user)
        association.delete()
        return Response({"message": "Vendeur retiré de votre espace."}, status=204)

class SignupVendeurView(CreateAPIView):
    serializer_class = SignupVendeurSerializer
    permission_classes = [AllowAny]

class VendeurOwnerView(RetrieveModelMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            association = VendeurAssociation.objects.get(vendeur=request.user)
            proprietaire = association.proprietaire
            return Response({
                "proprietaire_id": proprietaire.id,
                "proprietaire_nom": f"{proprietaire.first_name} {proprietaire.last_name}"
            })
        except VendeurAssociation.DoesNotExist:
            return Response({"detail": "Aucun propriétaire associé."}, status=404)

class ListeVendeursDuProprioView(ListModelMixin, GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(
            is_seller=True,
            vendeurassociation__proprietaire=self.request.user
        )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)