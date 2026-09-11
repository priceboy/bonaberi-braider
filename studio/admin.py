from django.contrib import admin

from .models import BusinessProfile, Hairstyle


@admin.register(Hairstyle)
class HairstyleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "featured", "published", "created_at")
    list_filter = ("category", "featured", "published")
    search_fields = ("title", "slug", "caption")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-featured", "-created_at")


@admin.register(BusinessProfile)
class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "whatsapp_number", "address")