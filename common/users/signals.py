from allauth.account.signals import user_signed_up, email_confirmed
from django.core.mail import mail_admins
from django.dispatch import receiver


@receiver(user_signed_up)
def handle_user_signed_up(request, user, **kwargs):
    mail_admins(
        user.email + "-" + str(request.get_host()),
        "Email:" + user.email,
    )


@receiver(email_confirmed)
def handle_email_confirmed(sender, request, email_address, **kwargs):
    email_address.set_as_primary()
