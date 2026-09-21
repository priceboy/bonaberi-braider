from django.test import TestCase
from django.urls import reverse

from .models import BusinessProfile, Hairstyle


class BusinessProfileTests(TestCase):
    def test_seed_creates_profile(self):
        self.assertEqual(BusinessProfile.objects.count(), 1)

    def test_str(self):
        profile = BusinessProfile.objects.first()
        self.assertEqual(str(profile), profile.name)


class HairstyleTests(TestCase):
    def test_seed_creates_styles(self):
        self.assertEqual(Hairstyle.objects.count(), 6)

    def test_str(self):
        style = Hairstyle.objects.first()
        self.assertEqual(str(style), style.title)

    def test_display_image_falls_back_to_url(self):
        style = Hairstyle.objects.get(slug="editorial-updo")
        self.assertEqual(style.display_image(), style.image_url)


class HomeViewTests(TestCase):
    def test_home_renders(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Phanie Magic Touch")
        self.assertContains(response, "Sculpted Knotless Braids")

    def test_home_includes_categories(self):
        response = self.client.get(reverse("home"))
        for category in ["Braids", "Locs", "Twists", "Wigs", "Natural Hair", "Other"]:
            self.assertContains(response, category)

    def test_unpublished_styles_hidden(self):
        Hairstyle.objects.update(published=False)
        response = self.client.get(reverse("home"))
        self.assertNotContains(response, "Sculpted Knotless Braids")


class StyleDetailViewTests(TestCase):
    def test_detail_renders(self):
        style = Hairstyle.objects.get(slug="sculpted-knotless-braids")
        response = self.client.get(reverse("style_detail", args=[style.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, style.title)

    def test_unpublished_detail_404s(self):
        style = Hairstyle.objects.get(slug="sculpted-knotless-braids")
        style.published = False
        style.save()
        response = self.client.get(reverse("style_detail", args=[style.slug]))
        self.assertEqual(response.status_code, 404)