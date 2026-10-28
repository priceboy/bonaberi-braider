from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Category, Hairstyle, SiteConfiguration


class PublicPageTests(TestCase):
    def test_home_renders_seeded_demo_portraits(self):
        response = self.client.get(reverse("website:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Book on WhatsApp")
        self.assertContains(response, "https://wa.me/237672748984")
        self.assertContains(response, "Salon name to be confirmed")
        self.assertContains(response, "Sculpted Knotless Braids")
        self.assertContains(response, "Demo photo")
        self.assertNotContains(response, 'href="#"')

    def test_work_page_renders_demo_gallery(self):
        response = self.client.get(reverse("website:our_work"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Demo gallery")
        self.assertContains(response, "Sculpted Knotless Braids")
        self.assertContains(response, "data-gallery-item")

    def test_work_page_renders_empty_gallery_when_no_images_exist(self):
        Hairstyle.objects.all().delete()
        response = self.client.get(reverse("website:our_work"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The gallery will appear")

    def test_find_us_page_renders_without_location_configuration(self):
        response = self.client.get(reverse("website:find_us"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Map to be configured")

    def test_site_configuration_controls_brand_booking_and_location(self):
        SiteConfiguration.objects.create(
            salon_name="Confirmed Salon",
            tagline="Confirmed tagline",
            hero_title="A confirmed headline",
            hero_text="Confirmed description",
            booking_url="https://wa.me/237672748984",
            address="Owner-supplied address",
            map_open_url="https://maps.google.com/?q=example",
        )
        home = self.client.get(reverse("website:home"))
        find_us = self.client.get(reverse("website:find_us"))
        self.assertContains(home, "Confirmed Salon")
        self.assertContains(home, "https://wa.me/237672748984")
        self.assertContains(home, "Book on WhatsApp")
        self.assertContains(home, "floating-booking")
        self.assertContains(find_us, "Owner-supplied address")
        self.assertContains(find_us, "https://maps.google.com/?q=example")
        self.assertFalse(find_us.context["location_configured"])


class HairstyleModelTests(TestCase):
    def setUp(self):
        self.category, _ = Category.objects.get_or_create(name="Braids")

    def test_category_slug_is_generated(self):
        self.assertEqual(self.category.slug, "braids")

    def test_image_is_optional_until_owner_uploads_assets(self):
        style = Hairstyle.objects.create(title="Knotless braids", category=self.category)
        self.assertEqual(style.display_image(), "")

    def test_uploaded_image_url_is_available(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        style = Hairstyle.objects.create(
            title="Knotless braids", category=self.category,
            image=SimpleUploadedFile("style.jpg", b"test-image", content_type="image/jpeg"),
        )
        self.assertTrue(style.display_image().endswith("style.jpg"))

    def test_demo_image_url_is_used_when_no_upload_exists(self):
        style = Hairstyle.objects.create(
            title="Demo braid", category=self.category,
            image_url="https://images.unsplash.com/example.jpg", is_demo=True,
        )
        self.assertEqual(style.display_image(), "https://images.unsplash.com/example.jpg")

    def test_uploaded_image_takes_priority_over_demo_url(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        style = Hairstyle.objects.create(
            title="Uploaded braid", category=self.category,
            image=SimpleUploadedFile("real.jpg", b"test-image", content_type="image/jpeg"),
            image_url="https://images.unsplash.com/example.jpg", is_demo=True,
        )
        self.assertTrue(style.display_image().endswith("real.jpg"))

    def test_home_selection_validation_rejects_seventh_active_style(self):
        Hairstyle.objects.all().delete()
        for index in range(6):
            Hairstyle.objects.create(title=f"Style {index}", category=self.category, show_on_home=True)
        seventh = Hairstyle(title="Style 7", category=self.category, show_on_home=True)
        with self.assertRaises(ValidationError):
            seventh.full_clean()

    def test_site_configuration_is_a_single_record(self):
        first = SiteConfiguration.objects.create(salon_name="First")
        SiteConfiguration.objects.create(salon_name="Second")
        self.assertEqual(SiteConfiguration.objects.count(), 1)
        self.assertEqual(SiteConfiguration.objects.get().pk, first.pk)
        self.assertEqual(SiteConfiguration.objects.get().salon_name, "Second")
