"""
The mixins file of stock app
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.mixins import (ListModelMixin, CreateModelMixin,
                                   UpdateModelMixin, RetrieveModelMixin,
                                   DestroyModelMixin)
from rest_framework.generics import GenericAPIView
from .models import Article, Boutique, PointDeVente
from .serializers import ArticleSerializer, BoutiqueSerializer, PointDeVenteSerializer

CREATED = "Création reussi"
DELETED = "Suppression reussi"
MODIFIED = "Modification reussi"

#Views for Store
class CreateBoutique(CreateModelMixin, GenericAPIView):
    """
    Create a new store
    """
    queryset = Boutique.objects.all()
    serializer_class = BoutiqueSerializer

    def post(self, request, *args, **kwargs):
        """
        post a new store
        """
        response = self.create(request, *args, **kwargs)

        if response.status_code == status.HTTP_201_CREATED:
            return Response({
                "message": f"{CREATED}"
            }, status=status.HTTP_201_CREATED)
        return response

class ListBoutique(ListModelMixin, GenericAPIView):
    """
    List store
    """
    queryset = Boutique.objects.all()
    serializer_class = BoutiqueSerializer

    def get(self, request, *args, **kwargs):
        """
        get all stores
        """
        return self.list(request, *args, **kwargs)

class DetailBoutique(RetrieveModelMixin, GenericAPIView):
    """
    Detail of boutique
    """
    queryset = Boutique.objects.all()
    serializer_class = BoutiqueSerializer

    def get(self, request, *args, **kwargs):
        """
        Get one store
        """
        if kwargs.get('pk'):
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs) 

class UpdateBoutique(UpdateModelMixin, GenericAPIView):
    """
    Update one store
    """
    queryset = Boutique.objects.all()  
    serializer_class = BoutiqueSerializer

    def put(self, request, *args, **kwargs):
        """
        update all files of store's database
        """
        response = self.update(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            return Response({
                "message":f"{MODIFIED}"
            }, status=status.HTTP_200_OK)
        return response

    def patch(self, request, *args, **kwargs):
        """
        Update just part of store's database
        """
        response = self.partial_update(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            return Response({
                "message": "Boutique modifié"
            }, status=status.HTTP_200_OK)
        return response

class DeleteBoutique(DestroyModelMixin, GenericAPIView):
    """
    Delete one store
    """
    queryset = Boutique.objects.all()
    serializer_class = BoutiqueSerializer

    def delete(self, request, *args,**kwargs):
        """
        Delete a store in database
        """
        response = self.destroy(request, *args, **kwargs)

        if response.status_code == status.HTTP_204_NO_CONTENT:
            return Response({
                "message": f"{DELETED}"
            }, status=status.HTTP_204_NO_CONTENT)
        return response

class BoutiqueAction(UpdateBoutique,
                     DetailBoutique,
                     DeleteBoutique):
    """
    A combine class of all action for store  
    """


#Views of points de vente
class CreatePointDeVente(CreateModelMixin,GenericAPIView):
    """
    Create a new store site
    """
    queryset = PointDeVente.objects.all() # pylint: disable=no-member
    serializer_class = PointDeVenteSerializer

    def post(self, request, *args, **kwargs):
        """
        post a new store site
        """
        response = self.create(request, *args, **kwargs)

        if response.status_code == status.HTTP_201_CREATED:
            return Response({
                "message": f"{CREATED}"
            }, status=status.HTTP_201_CREATED)

class ListPointVente(ListModelMixin, GenericAPIView):
    """
    List of store site
    """
    queryset = PointDeVente.objects.all()
    serializer_class = PointDeVenteSerializer

    def get(self, request, *args, **kwargs):
        """
        Get all store site
        """
        return self.list(request, *args, **kwargs)

class DetailPointVente(RetrieveModelMixin, GenericAPIView):
    """
    Details of one store site
    """
    queryset=PointDeVente.objects.all()
    serializer_class=PointDeVenteSerializer

    def get(self, request, *args, **kwargs):
        """
        Get one store site
        """
        return self.retrieve(request, *args, **kwargs)
    
class UpdatePointVente(UpdateModelMixin, GenericAPIView):
    """
    Update store site
    """
    queryset = PointDeVente.objects.all()
    serializer_class= PointDeVenteSerializer

    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            return Response({
                "message": f"{MODIFIED}"
            }, status=status.HTTP_200_OK)
        return response
    
    def patch(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            return Response({
                "message": f"{MODIFIED}"
            }, status=status.HTTP_200_OK)
        return response

class DeletePointVente(DestroyModelMixin, GenericAPIView):
    """
    Delete a store site
    """
    queryset=PointDeVente.objects.all()
    serializer_class = PointDeVenteSerializer

    def delete(self, request, *args, **kwargs):
        """
        Delete store site
        """
        response = self.destroy(request, *args, **kwargs)

        if response.status_code == status.HTTP_204_NO_CONTENT:
            return Response({
                "message": f"{DELETED}"
            }, status=status.HTTP_204_NO_CONTENT)
        return response

class PointVenteAction(UpdatePointVente,
                       DeletePointVente,
                       DetailPointVente):
    """
    All action to one store site
    """

#Views of articles
class ArticleList(ListModelMixin, GenericAPIView):
    """
    List all articles
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request, *args,**kwargs):
        return self.list(request, *args, **kwargs)
