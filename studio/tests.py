from django.test import TestCase
from django.urls import reverse


class LegacyStudioRouteTests(TestCase):
    def test_old_studio_home_redirects_to_canonical_home(self):
        response = self.client.get(reverse("studio:home"))
        self.assertRedirects(response, reverse("website:home"), status_code=301)

    def test_old_style_detail_route_redirects_to_canonical_portfolio(self):
        response = self.client.get(reverse("studio:style_detail", args=["old-style-slug"]))
        self.assertRedirects(response, reverse("website:our_work"), status_code=301)
