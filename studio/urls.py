from django.urls import path
from django.views.generic import RedirectView

app_name = "studio"

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="website:home", permanent=True), name="home"),
    # The legacy detail route includes a slug; use a fixed destination so it
    # is not accidentally passed as a keyword to the portfolio URL.
    path(
        "style/<slug:slug>/",
        RedirectView.as_view(url="/our-work/", permanent=True),
        name="style_detail",
    ),
]
