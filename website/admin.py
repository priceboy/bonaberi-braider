from django.contrib import admin
from django.utils.html import format_html

from .models import Category, DirectionStep, Hairstyle, SiteConfiguration


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Brand", {"fields": ("salon_name", "tagline", "hero_title", "hero_text")}),
        ("Home page", {"fields": ("home_background", "booking_url")}),
        ("Location", {"fields": ("address", "map_embed_url", "map_open_url")}),
    )

    def has_add_permission(self, request):
        return super().has_add_permission(request) and not SiteConfiguration.objects.exists()


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Hairstyle)
class HairstyleAdmin(admin.ModelAdmin):
    list_display = [
        "title", "category", "is_active", "show_on_home",
        "show_in_carousel", "sort_order", "thumbnail",
    ]
    list_editable = ["sort_order", "show_on_home", "show_in_carousel", "is_active"]
    list_filter = ["category", "is_active", "show_on_home", "show_in_carousel"]
    search_fields = ["title", "description"]
    ordering = ["sort_order", "created_at"]
    fields = [
        "title", "category", "image", "description",
        "show_on_home", "show_in_carousel", "is_active", "sort_order",
    ]

    @admin.display(description="Image")
    def thumbnail(self, obj):
        image_url = obj.display_image()
        if image_url:
            return format_html(
                '<img src="{}" alt="" style="height:60px;width:60px;object-fit:cover;" />',
                image_url,
            )
        return "No image"


@admin.register(DirectionStep)
class DirectionStepAdmin(admin.ModelAdmin):
    list_display = ["order", "title", "is_active"]
    list_editable = ["is_active"]
    list_display_links = ["title"]
    ordering = ["order"]
