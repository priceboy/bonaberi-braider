from django.contrib import admin

from .models import BusinessProfile, Hairstyle, StyleImage


class StyleImageInline(admin.TabularInline):
    model = StyleImage
    extra = 1
    fields = ("image", "image_url", "position", "caption")
    ordering = ("position", "id")


@admin.register(Hairstyle)
class HairstyleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "photos", "featured", "published", "created_at")
    list_filter = ("category", "featured", "published")
    search_fields = ("title", "slug", "caption")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-featured", "-created_at")
    inlines = (StyleImageInline,)

    @admin.display(description="Photos")
    def photos(self, obj):
        total = obj.images.count()
        return total + 1 if obj.display_image() else total


@admin.register(StyleImage)
class StyleImageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "hairstyle", "position")
    list_filter = ("hairstyle__category",)
    ordering = ("hairstyle", "position", "id")


@admin.register(BusinessProfile)
class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "whatsapp_number", "address")
