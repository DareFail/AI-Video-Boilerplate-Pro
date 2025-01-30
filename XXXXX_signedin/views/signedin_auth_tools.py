from allauth.account.utils import send_email_confirmation
from allauth.account import app_settings
from allauth.account.models import EmailAddress
from sesame.utils import get_token, get_user

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from common.customGroups.decorators import signedin, admin
from common.users.models import CustomUser
from common.users.forms import CustomUserChangeForm
from common.customGroups.invitations import (
    process_invitation,
    clear_invite_from_session,
)
from common.customGroups.models import Invitation, Membership
from common.customGroups.roles import is_member, ROLE_ADMIN
from common.customGroups.forms import MembershipForm, set_form_fields_disabled

from ..forms import HijackUserForm
from ..utils import (
    get_website_from_app,
    render_with_appname,
    render_to_string_with_appname,
)


@user_passes_test(lambda u: u.is_authenticated, login_url="/")
def change_email(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user_before_update = CustomUser.objects.get(pk=user.pk)
            need_to_confirm_email = (
                user_before_update.email != user.email
                and settings.ACCOUNT_EMAIL_VERIFICATION
                == app_settings.EmailVerificationMethod.MANDATORY
                and not user_has_confirmed_email_address(user, user.email)
            )
            if need_to_confirm_email:
                new_email = user.email
                send_email_confirmation(
                    request, user, signup=False, email=new_email
                )
                user.email = user_before_update.email
                form = CustomUserChangeForm(instance=user)
            user.save()
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render_with_appname(
        request,
        "account/change_email.html",
        {
            "form": form,
        },
    )


def send_magic_link(request):
    if request.method == "POST":
        email = request.POST.get("email", "")
        user = CustomUser.objects.filter(email=email.lower()).first()
        if user:
            magic_token = get_token(user)
            magic_link = request.build_absolute_uri(
                f"{reverse('auth_magic_link', kwargs={'sesame': magic_token})}"
            )
            email_context = {
                "magic_link": magic_link,
            }
            send_mail(
                subject="Login",
                message=render_to_string_with_appname(
                    "account/email/other/magic_link.txt",
                    context=email_context,
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
                html_message=render_to_string_with_appname(
                    "account/email/other/magic_link.html",
                    context=email_context,
                ),
            )

    messages.success(
        request, "Please check your email for your one time login link."
    )
    return HttpResponseRedirect(reverse("account_login"))


def auth_magic_link(request, sesame):
    user = get_user(sesame)
    if user is None:
        return HttpResponseRedirect(reverse("home"))
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    user.save()
    return HttpResponseRedirect(reverse("home"))


def user_has_confirmed_email_address(user, email):
    try:
        email_obj = EmailAddress.objects.get_for_user(user, email)
        return email_obj.verified
    except EmailAddress.DoesNotExist:
        return False


@user_passes_test(lambda u: u.is_superuser, login_url="/")
def hijack(request):
    form = HijackUserForm()
    return render_with_appname(
        request,
        "account/hijack.html",
        {
            "form": form,
            "redirect_url": settings.LOGIN_REDIRECT_URL,
        },
    )


def send_invitation(invitation):
    email_context = {
        "invitation": invitation,
        "website": get_website_from_app(),
    }
    send_mail(
        subject="You're invited",
        message=render_to_string_with_appname(
            "account/email/other/invitation.txt", context=email_context
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[invitation.email],
        fail_silently=False,
        html_message=render_to_string_with_appname(
            "account/email/other/invitation.html", context=email_context
        ),
    )


@login_required
def list_groups(request):
    return render_with_appname(
        request,
        "account/list_groups.html",
        {},
    )


@signedin
def manage_group(request, group_unique):
    # group = request.group
    return render_with_appname(
        request,
        "account/manage_group.html",
        {},
    )


@signedin
def group_membership_details(request, group_unique, membership_id):
    membership = get_object_or_404(
        Membership, group=request.group, pk=membership_id
    )
    editing_self = membership.user == request.user
    can_edit_group_members = request.group_membership.is_admin()
    if not can_edit_group_members and not editing_self:
        messages.error(
            request, "Sorry, you don't have permission to access that page."
        )
        return HttpResponseRedirect(
            reverse("manage_group", args=[request.group.unique_code])
        )

    if request.method == "POST":
        if can_edit_group_members and not editing_self:
            membership_form = MembershipForm(request.POST, instance=membership)
            if membership_form.is_valid():
                membership = membership_form.save()
                messages.success(
                    request,
                    "Role for "
                    + membership.user.get_display_name()
                    + " updated.",
                )
    else:
        membership_form = MembershipForm(instance=membership)
    if editing_self:
        set_form_fields_disabled(membership_form)
    return render_with_appname(
        request,
        "account/group_membership_details.html",
        {
            "membership": membership,
            "membership_form": membership_form,
            "editing_self": editing_self,
        },
    )


@signedin
@require_POST
def remove_group_membership(request, group_unique, membership_id):
    membership = get_object_or_404(
        Membership, group=request.group, pk=membership_id
    )
    removing_self = membership.user == request.user
    can_edit_group_members = request.group_membership.is_admin()
    if not can_edit_group_members:
        if not removing_self:
            return HttpResponseRedirect(reverse("signedin_home", args=[group_unique]))
    if membership.role == ROLE_ADMIN:
        admin_count = Membership.objects.filter(
            group=request.group, role=ROLE_ADMIN
        ).count()
        if admin_count == 1:
            messages.error(
                request,
                "You cannot remove the only administrator from a group. "
                "Make another group member an administrator and try again.",
            )
            return HttpResponseRedirect(
                reverse("manage_group", args=[request.group.unique_code])
            )

    membership.delete()
    messages.success(
        request,
        membership.user.get_display_name()
        + " was removed from "
        + request.group.name,
    )
    if removing_self:
        return HttpResponseRedirect(reverse("home"))
    else:
        return HttpResponseRedirect(
            reverse("manage_group", args=[request.group.unique_code])
        )


@admin
@require_POST
def resend_invitation(request, group_unique, invitation_unique):
    invitation = get_object_or_404(
        Invitation, group=request.group, unique_code=invitation_unique
    )
    send_invitation(invitation)
    return HttpResponse("")


def accept_invitation(request, invitation_unique):
    invitation = get_object_or_404(Invitation, unique_code=invitation_unique)
    if not invitation.is_accepted:
        request.session["invitation_unique"] = invitation_unique
    else:
        clear_invite_from_session(request)
    if request.user.is_authenticated and is_member(
        request.user, invitation.group
    ):
        messages.info(
            request, "You are already a member of " + invitation.group.name
        )
        return HttpResponseRedirect(
            reverse("signedin_home", args=[invitation.group.unique_code])
        )

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(
                request, "Please log in again to accept your invitation."
            )
            return HttpResponseRedirect(reverse("account_login"))
        else:
            if invitation.is_accepted:
                messages.error(
                    request,
                    "Sorry, it looks like that invitation link has expired.",
                )
                return HttpResponseRedirect(reverse("home"))
            else:
                process_invitation(invitation, request.user)
                clear_invite_from_session(request)
                messages.success(
                    request,
                    "You successfully joined " + invitation.group.name,
                )
                return HttpResponseRedirect(
                    reverse(
                        "signedin_home", args=[invitation.group.unique_code]
                    )
                )

    return render_with_appname(
        request,
        "account/accept_invite.html",
        {
            "invitation": invitation,
        },
    )
