from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from .utils import get_app_directory
from . import views

base_directory = get_app_directory()


urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", views.home, name="home"),
        path("accounts/", include("allauth.urls")),
        path(
            "account/email/",
            views.change_email,
            name="change_email",
        ),
        path("groups/", views.list_groups, name="list_groups"),
        path(
            "account/<str:group_unique>/manage/",
            views.manage_group,
            name="manage_group",
        ),
        path(
            "account/<str:group_unique>/members/<int:membership_id>/",
            views.group_membership_details,
            name="group_membership_details",
        ),
        path(
            "account/<str:group_unique>/members/<int:membership_id>/remove/",
            views.remove_group_membership,
            name="remove_group_membership",
        ),
        path(
            "account/<str:group_unique>/invite/<str:invitation_unique>/",
            views.resend_invitation,
            name="resend_invitation",
        ),
        path(
            "account/<str:group_unique>/",
            views.signedin_home,
            name="signedin_home",
        ),
        path(
            "invitation/<str:invitation_id>/",
            views.accept_invitation,
            name="accept_invitation",
        ),
        path("magic/", views.send_magic_link, name="send_magic_link"),
        path(
            "magic/<str:sesame>/",
            views.auth_magic_link,
            name="auth_magic_link",
        ),
        path("hijack/", views.hijack, name="hijack"),
        path("hijack/", include("hijack.urls", namespace="hijack")),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
