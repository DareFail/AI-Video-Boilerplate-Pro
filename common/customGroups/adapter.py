from django.urls import reverse
from django.conf import settings

from allauth.account import app_settings
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_email, user_field

from ..utils import appname_from_request
from .invitations import clear_invite_from_session

# Overwrite
# https://github.com/pennersr/django-allauth/blob/87edc03effd8b2932294f1da23e766a8b1adf2ee/allauth/account/adapter.py


class CustomAccountAdapter(DefaultAccountAdapter):

    def populate_username(self, request, user):
        user_field(
            user, app_settings.USER_MODEL_USERNAME_FIELD, user_email(user)
        )

    def get_login_redirect_url(self, request):
        from .models import Invitation

        if request.session.get("invitation_unique"):
            invitation_unique = request.session.get("invitation_unique")
            try:
                invite = Invitation.objects.get(unique_code=invitation_unique)
                if not invite.is_accepted:
                    return reverse(
                        "accept_invitation",
                        args=[request.session["invitation_unique"]],
                    )
                else:
                    clear_invite_from_session(request)
            except Invitation.DoesNotExist:
                pass
        else:
            try:
                foundGroup = (
                    request.user.customGroups.filter(
                        main_service=request.get_host()
                    )
                    .first()
                    .dashboard_url
                )
                return foundGroup
            except Exception as e:
                print(e)
                pass
        return super(CustomAccountAdapter, self).get_login_redirect_url(
            request
        )

    def get_email_confirmation_url(self, request, emailconfirmation):
        next_url = request.POST.get("next")
        request.session["next_on_email_confirmation"] = next_url

        email_conf_url = super(
            CustomAccountAdapter, self
        ).get_email_confirmation_url(request, emailconfirmation)
        return email_conf_url

    def get_email_verification_redirect_url(self, email_address):
        if "next_on_email_confirmation" in self.request.session:
            return self.request.session["next_on_email_confirmation"]
        else:
            return super(
                CustomAccountAdapter, self
            ).get_email_verification_redirect_url(email_address)

    def format_email_subject(self, subject):
        new_subject = "[" + self.request.get_host() + "] " + subject

        return super(CustomAccountAdapter, self).format_email_subject(
            new_subject
        )

    def send_mail(self, template_prefix, email, context):

        ctx = {
            "HOST": self.request.get_host(),
            "APP_DIRECTORY": appname_from_request(self.request),
        }

        ctx.update(context)

        return super(CustomAccountAdapter, self).send_mail(
            template_prefix, email, ctx
        )

    def get_from_email(self):
        return settings.DEFAULT_FROM_EMAIL


# Overwrite
# https://github.com/pennersr/django-allauth/blob/87edc03effd8b2932294f1da23e766a8b1adf2ee/allauth/socialaccount/adapter.py


class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def is_open_for_signup(self, request, sociallogin):
        return True

    def populate_user(self, request, sociallogin, data):
        return request.resolver_match.app_name

    def is_auto_signup_allowed(self, request, sociallogin):
        return True

    def get_connect_redirect_url(self, request, socialaccount):
        if "group" in request.session:
            try:
                foundGroup = (
                    request.user.customGroups.filter(
                        main_service=request.get_host(),
                        id=request.session["group"],
                    )
                    .first()
                    .dashboard_url
                )
                return foundGroup
            except Exception as e:
                print(e)
                del request.session["group"]
                pass
        return str(request.get_host())
