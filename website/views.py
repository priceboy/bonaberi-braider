from django.db.models import Q
from django.shortcuts import render
from urllib.parse import quote_plus

from .models import Category, DirectionStep, Hairstyle, SiteConfiguration


# Confirmed salon pin. Admin-configured map URLs can override these defaults.
SALON_LATITUDE = "4.09235"
SALON_LONGITUDE = "9.64496"
SALON_COORDINATES = f"{SALON_LATITUDE}, {SALON_LONGITUDE}"
DEFAULT_MAP_EMBED_URL = f"https://www.google.com/maps?q={SALON_COORDINATES}&output=embed"
DEFAULT_MAP_OPEN_URL = f"https://www.google.com/maps?q={SALON_COORDINATES}"


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
    steps = DirectionStep.objects.filter(
        is_active=True,
    ).filter(
        Q(site_configuration=config) | Q(site_configuration__isnull=True)
    ).order_by("order", "id")
    map_embed_url = (
        config.map_embed_url if config and config.map_embed_url
        else DEFAULT_MAP_EMBED_URL
    )
    map_open_url = (
        config.map_open_url if config and config.map_open_url
        else config.map_embed_url if config and config.map_embed_url
        else DEFAULT_MAP_OPEN_URL
    )
    address = (
        config.address if config and config.address
        else f"{SALON_LATITUDE}° N, {SALON_LONGITUDE}° E"
    )
    map_destination = config.address if config and config.address else SALON_COORDINATES
    map_ios_url = f"https://maps.apple.com/?daddr={quote_plus(map_destination)}"
    return render(
        request,
        "website/find_us.html",
        {
            "site_config": config,
            "map_embed_url": map_embed_url,
            "map_open_url": map_open_url,\n            "map_ios_url": map_ios_url,
            "address": address,
            "location_configured": True,
            "steps": steps,
        },
    )
