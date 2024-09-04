from django.utils.crypto import get_random_string

from .models import CustomGroup
from .roles import ROLE_ADMIN


def get_default_group_from_request(request):
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
        except CustomGroup.DoesNotExist:
            del request.session["group"]
            pass
    if request.user.customGroups.count():
        return request.user.customGroups.filter(
            main_service=request.get_host()
        ).first()
    else:
        return None


def create_default_group_for_user(user, group_name="Group", host=None):
    unique_code = get_random_string(length=16)
    main_service = host
    group = CustomGroup.objects.create(
        name=group_name, unique_code=unique_code, main_service=main_service
    )
    group.members.add(user, through_defaults={"role": ROLE_ADMIN})
    group.save()
    return group
