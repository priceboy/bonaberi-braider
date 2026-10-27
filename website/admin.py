from django.contrib import admin
from django.utils.html import format_html

from .models import Category, DirectionStep, Hairstyle


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Hairstyle)
class HairstyleAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "category",
        "is_active",
        "show_on_home",
        "show_in_carousel",
        "sort_order",
        "thumbnail",
    ]
    list_editable = ["sort_order", "show_on_home", "show_in_carousel", "is_active"]
    list_filter = ["category", "is_active", "show_on_home", "show_in_carousel"]
    search_fields = ["title", "description"]
    ordering = ["sort_order", "created_at"]

    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height: 60px; width: 60px; object-fit: cover;" />',
                obj.image.url,
            )
        return "-"
    thumbnail.short_description = "Image"


@admin.register(DirectionStep)
class DirectionStepAdmin(admin.ModelAdmin):
    list_display = ["order", "title", "is_active"]
    list_editable = ["is_active"]
    list_display_links = ["title"]
    ordering = ["order"]
