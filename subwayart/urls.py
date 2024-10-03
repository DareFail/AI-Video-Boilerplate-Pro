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
        path("hijack/", include("hijack.urls", namespace="hijack")),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
