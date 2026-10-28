from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


class SiteConfiguration(models.Model):
    """Editable public-site details. Leave unknown real-world information blank."""

    salon_name = models.CharField(max_length=120, blank=True, default="")
    tagline = models.CharField(max_length=200, blank=True, default="")
    hero_title = models.CharField(max_length=160, blank=True, default="")
    hero_text = models.CharField(max_length=400, blank=True, default="")
    home_background = models.ImageField(
        upload_to="site/", blank=True, null=True,
        help_text="Salon interior photo used behind the Home page content.",
    )
    booking_url = models.URLField(
        blank=True, default="",
        verbose_name="WhatsApp booking link",
        help_text=(
            "Use a WhatsApp click-to-chat URL, e.g. https://wa.me/237XXXXXXXXX "
            "(international number, digits only; no +, spaces, or dashes). "
            "Leave blank until the salon's number is confirmed."
        ),
    )
    address = models.CharField(max_length=250, blank=True, default="")
    map_embed_url = models.URLField(
        blank=True, default="",
        help_text="Optional map embed URL supplied by the owner.",
    )
    map_open_url = models.URLField(
        blank=True, default="",
        help_text="Optional public Google Maps or map-app destination.",
    )

    class Meta:
        verbose_name = "Site configuration"
        verbose_name_plural = "Site configuration"

    def __str__(self):
        return self.salon_name or "Site configuration"

    def save(self, *args, **kwargs):
        # Keep one configuration record without adding a dependency on a
        # third-party singleton package.
        if self.pk is None:
            existing = type(self).objects.order_by("pk").first()
            if existing:
                self.pk = existing.pk
                # QuerySet.create() passes force_insert=True. Once we reuse
                # the singleton row's primary key, this must become an update.
                kwargs.pop("force_insert", None)
        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            base = slugify(self.name) or "category"
            slug = base
            counter = 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Hairstyle(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="hairstyles"
    )
    image = models.ImageField(
        upload_to="hairstyles/", blank=True, null=True,
        help_text="Upload genuine salon work. Transparent PNG/WebP recommended for Home cutouts.",
    )
    description = models.CharField(max_length=300, blank=True, default="")
    show_on_home = models.BooleanField(default=False)
    show_in_carousel = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order", "created_at", "id"]

    def __str__(self):
        return self.title

    def display_image(self):
        return self.image.url if self.image else ""

    def clean(self):
        super().clean()
        if self.show_on_home and self.is_active:
            qs = Hairstyle.objects.filter(
                is_active=True, show_on_home=True
            ).exclude(pk=self.pk)
            if qs.count() >= 6:
                raise ValidationError(
                    "Only up to six active hairstyles can be marked to show on the Home page."
                )


class DirectionStep(models.Model):
    title = models.CharField(max_length=200, blank=True, default="")
    image = models.ImageField(upload_to="directions/", blank=True, null=True)
    instruction = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title or f"Step {self.order + 1}"
