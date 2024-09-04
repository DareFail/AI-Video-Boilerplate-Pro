from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.crypto import get_random_string

from .roles import ROLE_CHOICES, ROLE_ADMIN, ROLE_MEMBER


def generate_random_string():
    return get_random_string(length=16)


class CustomGroup(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    unique_code = models.CharField(
        max_length=100, default=generate_random_string, unique=True
    )
    main_service = models.CharField(max_length=100, null=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="customGroups",
        through="Membership",
    )
    show_groups = models.BooleanField(default=False)

    @property
    def dashboard_url(self):
        return reverse("signedin_home", args=[self.unique_code])


class Membership(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    group = models.ForeignKey(CustomGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    role = models.CharField(max_length=100, choices=ROLE_CHOICES)

    def is_admin(self):
        return self.role == ROLE_ADMIN


class Invitation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    unique_code = models.CharField(
        max_length=100, default=generate_random_string, unique=True
    )
    group = models.ForeignKey(
        CustomGroup, on_delete=models.CASCADE, related_name="invitations"
    )
    email = models.EmailField()
    role = models.CharField(
        max_length=100, choices=ROLE_CHOICES, default=ROLE_MEMBER
    )
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_invitations",
    )
    is_accepted = models.BooleanField(default=False)
    accepted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="accepted_invitations",
        null=True,
        blank=True,
    )

    def get_url(self):
        return reverse("accept_invitation", args=[self.id])
