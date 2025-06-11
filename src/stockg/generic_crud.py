"""
The mixins file of stock app
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.mixins import (ListModelMixin, CreateModelMixin,
                                   UpdateModelMixin, RetrieveModelMixin,
                                   DestroyModelMixin)
from rest_framework.generics import GenericAPIView

CREATED = "Création reussi"
DELETED = "Suppression reussi"
MODIFIED = "Modification reussi"

#Function for generic CRUD

def create_customized(model, serializer):
    """
    This function get a model and a serializer class and return the objet created
    """
    class CustomCreateView(CreateModelMixin, GenericAPIView):
        """
        Create something
        """
        queryset = model.objects.all()
        serializer_class = serializer
        permission_classes = [AllowAny]

        def post(self, request, *args,**kwargs):
            """
            post something
            """
            response = self.create(request, *args, **kwargs)

            if response.status_code == status.HTTP_201_CREATED:
                return Response({
                    "message": f"{CREATED}"
                }, status=status.HTTP_201_CREATED)
            return response
    return CustomCreateView

def list_customized(model, serializer):
    """
    This function get a model and a serializer class and return list of objet
    """
    class ListCustomView(ListModelMixin, GenericAPIView):
        """
        List something
        """
        queryset = model.objects.all()
        serializer_class = serializer

        def get(self, request, *args, **kwargs):
            """
            get all things
            """
            return self.list(request, *args, **kwargs)
    return ListCustomView

def detail_update_delete_customized(model, serializer):
    """
    This function get a model and a serializer class and return detail, update and delete object
    """
    class DetailCustomView(RetrieveModelMixin, GenericAPIView):
        """
        Detail of somthing
        """
        queryset = model.objects.all()
        serializer_class = serializer

        def get(self, request, *args, **kwargs):
            """
            Get one thing
            """
            if kwargs.get('pk'):
                return self.retrieve(request, *args, **kwargs)
    class UpdateCustomView(UpdateModelMixin, GenericAPIView):
        """
        Update something
        """
        queryset = model.objects.all()  
        serializer_class = serializer

        def put(self, request, *args, **kwargs):
            """
            update all files of something's database
            """
            response = self.update(request, *args, **kwargs)
            if response.status_code == status.HTTP_200_OK:
                return Response({
                    "message":f"{MODIFIED}"
                }, status=status.HTTP_200_OK)
            return response

        def patch(self, request, *args, **kwargs):
            """
            Update just part of something's database
            """
            response = self.partial_update(request, *args, **kwargs)
            if response.status_code == status.HTTP_200_OK:
                return Response({
                    "message": f"{MODIFIED}"
                }, status=status.HTTP_200_OK)
            return response
    class DeleteCustomView(DestroyModelMixin, GenericAPIView):
        """
        Delete one thing
        """
        queryset = model.objects.all()
        serializer_class = serializer

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
    class CombineActionView(UpdateCustomView,
                     DetailCustomView,
                     DeleteCustomView):
        """
        all action
        """
    return CombineActionView
