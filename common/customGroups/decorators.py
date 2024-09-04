from functools import wraps
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import CustomGroup, Membership
from .roles import is_member, is_admin
from common.utils import appname_from_request


def signedin(view_func):
    @wraps(view_func)
    def _inner(request, *args, **kwargs):
        user = request.user
        unique_code = kwargs["group_unique"]

        if not user.is_authenticated:
            return HttpResponseRedirect(
                f'{reverse("account_login")}?next={request.path}'
            )
        else:
            group = get_object_or_404(CustomGroup, unique_code=unique_code)
            if is_member(user, group):
                request.group = group
                request.group_membership = Membership.objects.get(
                    group=group, user=user
                )
                request.session["group"] = group.id
                return view_func(request, *args, **kwargs)
            else:
                return render(request, appname_from_request(request))

    return _inner


def admin(view_func):
    @wraps(view_func)
    def _inner(request, *args, **kwargs):
        user = request.user
        unique_code = kwargs["group_unique"]

        if not user.is_authenticated:
            return HttpResponseRedirect(
                f'{reverse("account_login")}?next={request.path}'
            )
        else:
            group = get_object_or_404(CustomGroup, unique_code=unique_code)
            if is_admin(user, group):
                request.group = group
                request.group_membership = Membership.objects.get(
                    group=group, user=user
                )
                request.session["group"] = group.id
                return view_func(request, *args, **kwargs)
            else:
                return render(request, appname_from_request(request))

    return _inner
