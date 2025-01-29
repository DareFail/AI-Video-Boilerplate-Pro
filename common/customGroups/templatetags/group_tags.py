from django import template

from common.customGroups.roles import is_member, is_admin

from common.customGroups.helpers import create_default_group_for_user

register = template.Library()


@register.filter
def is_member_of(user, group):
    return is_member(user, group)


@register.filter
def is_admin_of(user, group):
    return is_admin(user, group)


@register.filter
def get_dashboard_url(request):
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
    elif not request.user.is_anonymous:
        newGroup = request.user.customGroups.filter(
            main_service=request.get_host()
        ).first()
        if newGroup is None:
            newGroup = create_default_group_for_user(
                request.user, host=request.get_host()
            )
            request.session["group"] = newGroup.id
        return newGroup.dashboard_url
    return str(request.get_host())


@register.filter
def get_group_unique_code(request):
    if "group" in request.session:
        try:
            foundGroup = (
                request.user.customGroups.filter(
                    main_service=request.get_host(),
                    id=request.session["group"],
                )
                .first()
                .unique_code
            )
            return foundGroup
        except Exception as e:
            print(e)
            del request.session["group"]
            pass
    elif not request.user.is_anonymous:
        newGroup = request.user.customGroups.filter(
            main_service=request.get_host()
        ).first()
        if newGroup is None:
            newGroup = create_default_group_for_user(
                request.user, host=request.get_host()
            )
            request.session["group"] = newGroup.id
        return newGroup.unique_code
    return str(request.get_host())


@register.filter
def get_ordered_organizations(request):
    if "group" in request.session:
        try:
            foundGroup = (
                request.user.customGroups.filter(
                    main_service=request.get_host()
                ).all()
            )
            return foundGroup
        except Exception as e:
            print(e)
            del request.session["group"]
            pass
    elif not request.user.is_anonymous:
        newGroup = request.user.customGroups.filter(
            main_service=request.get_host()
        ).all()
        return newGroup
    return []
