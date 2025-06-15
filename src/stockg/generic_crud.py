"""
The mixins file of stock app
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import (ListModelMixin, CreateModelMixin,
                                   UpdateModelMixin, RetrieveModelMixin,
                                   DestroyModelMixin)
from rest_framework.generics import GenericAPIView

CREATED = "Création reussie"
DELETED = "Suppression reussie"
MODIFIED = "Modification reussie"

# Fonction pour retrouver le bon utilisateur (propriétaire réel)
def get_proprio_user(user):
    if hasattr(user, 'vendeurassociation'):
        return user.vendeurassociation.proprietaire
    return user

# 🔹 CREATE
def create_customized(model, serializer):
    class CustomCreateView(CreateModelMixin, GenericAPIView):
        queryset = model.objects.all()
        serializer_class = serializer
        permission_classes = [IsAuthenticated]

        def perform_create(self, serializer):
            user = get_proprio_user(self.request.user)
            serializer.save(proprietaire=user)

        def post(self, request, *args, **kwargs):
            response = self.create(request, *args, **kwargs)
            if response.status_code == status.HTTP_201_CREATED:
                return Response({"message": f"{CREATED}"}, status=status.HTTP_201_CREATED)
            return response
    return CustomCreateView

# 🔹 LIST
def list_customized(model, serializer):
    class ListCustomView(ListModelMixin, GenericAPIView):
        serializer_class = serializer
        permission_classes = [IsAuthenticated]

        def get_queryset(self):
            user = get_proprio_user(self.request.user)
            return model.objects.filter(proprietaire=user)

        def get(self, request, *args, **kwargs):
            return self.list(request, *args, **kwargs)
    return ListCustomView

# 🔹 DETAIL / UPDATE / DELETE
def detail_update_delete_customized(model, serializer):
    class BaseView(GenericAPIView):
        serializer_class = serializer
        permission_classes = [IsAuthenticated]

        def get_queryset(self):
            user = get_proprio_user(self.request.user)
            return model.objects.filter(proprietaire=user)

    class DetailCustomView(RetrieveModelMixin, BaseView):
        def get(self, request, *args, **kwargs):
            return self.retrieve(request, *args, **kwargs)

    class UpdateCustomView(UpdateModelMixin, BaseView):
        def put(self, request, *args, **kwargs):
            response = self.update(request, *args, **kwargs)
            if response.status_code == status.HTTP_200_OK:
                return Response({"message": f"{MODIFIED}"}, status=status.HTTP_200_OK)
            return response

        def patch(self, request, *args, **kwargs):
            response = self.partial_update(request, *args, **kwargs)
            if response.status_code == status.HTTP_200_OK:
                return Response({"message": f"{MODIFIED}"}, status=status.HTTP_200_OK)
            return response

    class DeleteCustomView(DestroyModelMixin, BaseView):
        def delete(self, request, *args, **kwargs):
            response = self.destroy(request, *args, **kwargs)
            if response.status_code == status.HTTP_204_NO_CONTENT:
                return Response({"message": f"{DELETED}"}, status=status.HTTP_204_NO_CONTENT)
            return response

    class CombineActionView(UpdateCustomView, DetailCustomView, DeleteCustomView):
        pass

    return CombineActionView
