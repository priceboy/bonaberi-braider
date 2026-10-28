"""URL configuration for the Phanie Magic Touch website."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(("website.urls", "website"), namespace="website")),
    # Keep old links working while directing visitors to the canonical pages.
    path("studio/", include(("studio.urls", "studio"), namespace="studio")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
