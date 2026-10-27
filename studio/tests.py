from django.test import TestCase
from django.urls import reverse

from .models import BusinessProfile, Hairstyle, StyleImage


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

    def test_display_images_includes_cover(self):
        style = Hairstyle.objects.get(slug="editorial-updo")
        self.assertEqual(style.display_images(), [style.image_url])
        self.assertEqual(style.image_count, 1)


class StyleImageTests(TestCase):
    def setUp(self):
        self.style = Hairstyle.objects.get(slug="editorial-updo")

    def test_photos_are_ordered_by_position(self):
        second = StyleImage.objects.create(
            hairstyle=self.style, image_url="https://example.com/b.jpg", position=1
        )
        first = StyleImage.objects.create(
            hairstyle=self.style, image_url="https://example.com/a.jpg", position=0
        )
        self.assertEqual(self.style.display_images(), [self.style.image_url, first.image_url, second.image_url])

    def test_duplicate_cover_is_not_repeated(self):
        StyleImage.objects.create(hairstyle=self.style, image_url=self.style.image_url)
        self.assertEqual(self.style.display_images(), [self.style.image_url])

    def test_empty_photos_are_skipped(self):
        StyleImage.objects.create(hairstyle=self.style)
        self.assertEqual(self.style.display_images(), [self.style.image_url])

    def test_cascade_delete_with_style(self):
        StyleImage.objects.create(hairstyle=self.style, image_url="https://example.com/a.jpg")
        self.style.delete()
        self.assertEqual(StyleImage.objects.count(), 0)

    def test_str(self):
        shot = StyleImage.objects.create(hairstyle=self.style, image_url="https://example.com/a.jpg")
        self.assertEqual(str(shot), f"{self.style.title} — photo 1")


class HomeViewTests(TestCase):
    def test_home_renders(self):
        response = self.client.get(reverse("studio:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Phanie Magic Touch")
        self.assertContains(response, "Sculpted Knotless Braids")

    def test_home_includes_categories(self):
        response = self.client.get(reverse("studio:home"))
        for category in ["Braids", "Locs", "Twists", "Wigs", "Natural Hair", "Other"]:
            self.assertContains(response, category)

    def test_unpublished_styles_hidden(self):
        Hairstyle.objects.update(published=False)
        response = self.client.get(reverse("studio:home"))
        self.assertNotContains(response, "Sculpted Knotless Braids")

    def test_photo_count_badge_shown_for_multi_photo_styles(self):
        style = Hairstyle.objects.get(slug="crown-loc-style")
        StyleImage.objects.create(hairstyle=style, image_url="https://example.com/a.jpg")
        StyleImage.objects.create(hairstyle=style, image_url="https://example.com/b.jpg")
        response = self.client.get(reverse("studio:home"))
        self.assertContains(response, "3 photos")


class StyleDetailViewTests(TestCase):
    def test_detail_renders(self):
        style = Hairstyle.objects.get(slug="sculpted-knotless-braids")
        response = self.client.get(reverse("studio:style_detail", args=[style.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, style.title)

    def test_detail_renders_every_photo(self):
        style = Hairstyle.objects.get(slug="crown-loc-style")
        StyleImage.objects.create(hairstyle=style, image_url="https://example.com/a.jpg")
        StyleImage.objects.create(hairstyle=style, image_url="https://example.com/b.jpg")
        response = self.client.get(reverse("studio:style_detail", args=[style.slug]))
        self.assertContains(response, "https://example.com/a.jpg")
        self.assertContains(response, "https://example.com/b.jpg")
        self.assertContains(response, "1 / 3")

    def test_unpublished_detail_404s(self):
        style = Hairstyle.objects.get(slug="sculpted-knotless-braids")
        style.published = False
        style.save()
        response = self.client.get(reverse("studio:style_detail", args=[style.slug]))
        self.assertEqual(response.status_code, 404)