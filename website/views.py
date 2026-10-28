from django.db.models import Q
from django.shortcuts import render

from .models import Category, DirectionStep, Hairstyle, SiteConfiguration


def site_configuration():
    return SiteConfiguration.objects.order_by("pk").first()


def with_images(queryset):
    """Only send records with uploaded or remote demo images to image templates."""
    return queryset.filter(Q(image__gt="") | Q(image_url__gt=""))


def home(request):
    config = site_configuration()
    portraits = (
        with_images(Hairstyle.objects.filter(is_active=True, show_on_home=True))
        .select_related("category")
        .order_by("sort_order", "created_at", "id")[:6]
    )
    return render(
        request,
        "website/home.html",
        {
            "site_config": config,
            "portraits": portraits,
            "home_bg_placeholder": not bool(config and config.home_background),
            "booking_url": (config.booking_url or "https://wa.me/237672748984") if config else "https://wa.me/237672748984",
            "salon_name": config.salon_name if config and config.salon_name else "",
            "tagline": config.tagline if config and config.tagline else "",
            "hero_title": config.hero_title if config and config.hero_title else "",
            "hero_text": config.hero_text if config and config.hero_text else "",
        },
    )


def our_work(request):
    base_queryset = (
        with_images(Hairstyle.objects.filter(is_active=True))
        .select_related("category")
        .order_by("sort_order", "created_at", "id")
    )
    return render(
        request,
        "website/our_work.html",
        {
            "site_config": site_configuration(),
            "carousel_items": base_queryset.filter(show_in_carousel=True),
            "gallery_items": base_queryset,
            "categories": Category.objects.all().order_by("name"),
        },
    )


def find_us(request):
    config = site_configuration()
    steps = DirectionStep.objects.filter(is_active=True).order_by("order", "id")
    return render(
        request,
        "website/find_us.html",
        {
            "site_config": config,
            "map_embed_url": config.map_embed_url if config else "",
            "map_open_url": (config.map_open_url or config.map_embed_url) if config else "",
            "address": config.address if config else "",
            "location_configured": bool(config and config.map_embed_url),
            "steps": steps,
        },
    )
