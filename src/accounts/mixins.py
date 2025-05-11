from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer



"""class SignUpView(CreateModelMixin, GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            return Response({
                "success": True
                }
                , status=status.HTTP_200_OK)
        return response
"""
def create_custom(model, serializer):
    class CustomCreateView(CreateModelMixin, GenericAPIView):
        queryset = model.objects.all()
        serializer_class = serializer

        def post(self, request, *args, **kwargs):
            response = self.create(request, *args, **kwargs)

            if response.status_code == status.HTTP_201_CREATED:
                return Response({
                    "message": "Création réussie"
                }, status=status.HTTP_201_CREATED)
            return response

    return CustomCreateView