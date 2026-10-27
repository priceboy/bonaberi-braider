from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            base = slugify(self.name)
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
    image = models.ImageField(upload_to="hairstyles/")
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
