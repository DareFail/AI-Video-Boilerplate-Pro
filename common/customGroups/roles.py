ROLE_ADMIN = "admin"
ROLE_MEMBER = "member"

ROLE_CHOICES = (
    (ROLE_ADMIN, "Administrator"),
    (ROLE_MEMBER, "Member"),
)


def is_member(user, group):
    return group.members.filter(id=user.id).exists()


def is_admin(user, group):
    from .models import Membership

    return Membership.objects.filter(
        group=group, user=user, role=ROLE_ADMIN
    ).exists()
