from allauth.account.signals import user_signed_up
from django.dispatch import receiver

from common.customGroups.models import Invitation
from .invitations import process_invitation, get_invitation_unique_from_request


@receiver(user_signed_up)
def handle_user_signed_up(request, user, **kwargs):
    invitation_unique = get_invitation_unique_from_request(request)
    if invitation_unique:
        try:
            invitation = Invitation.objects.get(unique_code=invitation_unique)
            process_invitation(invitation, user)
        except Invitation.DoesNotExist:
            pass
