from django.urls import path
from .models import Invitation
from .serializers import InvitationSerializer
from stockg.generic_crud import create_customized
from .views import AcceptInvitation


urlpatterns = [
    path("invite/", create_customized(Invitation, InvitationSerializer).as_view(), name="inviter"),
    path("invite/<int:id_invitation>/accept/", AcceptInvitation.as_view(), name="accept-invitation"),
]
