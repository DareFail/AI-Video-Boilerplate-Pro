from allauth.account.forms import SignupForm
from django import forms
from django.core.exceptions import ValidationError

from .models import Invitation, Membership
from .helpers import create_default_group_for_user


class GroupSignupForm(SignupForm):
    invitation_unique = forms.CharField(
        widget=forms.HiddenInput(), required=False
    )
    group_name = forms.CharField(
        label="Group Name (Optional)",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Group Name (Optional)"}),
        required=False,
    )

    def clean_group_name(self):
        group_name = self.cleaned_data["group_name"]
        invitation_unique = self.cleaned_data.get("invitation_unique")
        if not invitation_unique and not group_name:
            email = self.cleaned_data.get("email")
            if email is not None:
                group_name = f"{email.split('@')[0]}"
        return group_name

    def clean_invitation_unique(self):
        invitation_unique = self.cleaned_data.get("invitation_unique")
        if invitation_unique:
            try:
                invite = Invitation.objects.get(unique_code=invitation_unique)
                if invite.is_accepted:
                    raise forms.ValidationError(
                        "Your invitation link has expired."
                        "You will need a new invitation."
                    )
            except (Invitation.DoesNotExist, ValidationError):
                raise forms.ValidationError(
                    "Invalid invitation link."
                    "You will need a new invitation."
                )
        return invitation_unique

    def save(self, request):
        invitation_unique = self.cleaned_data["invitation_unique"]
        group_name = self.cleaned_data["group_name"]
        user = super().save(request)

        if invitation_unique:
            assert not group_name
        else:
            create_default_group_for_user(
                user, group_name, host=request.get_host()
            )

        return user


class MembershipForm(forms.ModelForm):

    class Meta:
        model = Membership
        fields = ("role",)


def set_form_fields_disabled(form, disabled=True):
    for field in form.fields:
        form.fields[field].disabled = disabled
