from django.db import models


class BusinessProfile(models.Model):
    name = models.CharField(max_length=100, default="Phanie Magic Touch")
    tagline = models.CharField(max_length=200, default="Hair artistry, made unforgettable.")
    hero_title = models.CharField(max_length=100, default="YOUR NEXT LOOK.")
    hero_text = models.CharField(
        max_length=300, default="Intentional styles, immaculate detail, and a look that stays with you."
    )
    whatsapp_number = models.CharField(max_length=30, default="237000000000")
    address = models.CharField(max_length=200, default="Your studio address, Douala, Cameroon")
    hours = models.JSONField(
        default=list,
        help_text='Each entry appears on its own line, e.g. ["Tue – Sat · 9:00 AM – 6:00 PM", "Sunday · By appointment"]',
    )
    directions_url = models.URLField(default="https://www.google.com/maps")
    instagram_url = models.URLField(default="https://instagram.com")

    class Meta:
        verbose_name = "Business profile"
        verbose_name_plural = "Business profiles"

    def __str__(self):
        return self.name


class Hairstyle(models.Model):
    CATEGORY_CHOICES = [
        ("Braids", "Braids"),
        ("Locs", "Locs"),
        ("Twists", "Twists"),
        ("Wigs", "Wigs"),
        ("Natural Hair", "Natural Hair"),
        ("Other", "Other"),
    ]

    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    caption = models.TextField(blank=True, default="")
    image_url = models.URLField(blank=True, default="", help_text="External image URL (e.g. Unsplash).")
    image = models.ImageField(
        upload_to="styles/", blank=True, null=True, help_text="Optional: upload a local image. Falls back to image_url."
    )
    published = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["-featured", "-created_at", "title"]
        verbose_name = "Hairstyle"
        verbose_name_plural = "Hairstyles"

    def __str__(self):
        return self.title

    def display_image(self):
        if self.image:
            return self.image.url
        return self.image_url