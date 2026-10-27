from django.shortcuts import render

from .models import Category, DirectionStep, Hairstyle


def home(request):
    portraits = (
        Hairstyle.objects.filter(is_active=True, show_on_home=True)
        .select_related("category")
        .order_by("sort_order", "created_at", "id")[:6]
    )
    context = {
        "portraits": portraits,
        "home_bg_placeholder": True,
        "booking_url": "#",
        "salon_name": "Phanie Magic Touch",
    }
    return render(request, "website/home.html", context)


def our_work(request):
    carousel_items = (
        Hairstyle.objects.filter(is_active=True, show_in_carousel=True)
        .select_related("category")
        .order_by("sort_order", "created_at", "id")
    )
    gallery_items = (
        Hairstyle.objects.filter(is_active=True)
        .select_related("category")
        .order_by("sort_order", "created_at", "id")
    )
    categories = Category.objects.all().order_by("name")
    context = {
        "carousel_items": carousel_items,
        "gallery_items": gallery_items,
        "categories": categories,
    }
    return render(request, "website/our_work.html", context)


def find_us(request):
    steps = DirectionStep.objects.filter(is_active=True).order_by("order", "id")
    context = {
        "map_embed_url": "",
        "map_open_url": "",
        "address": "",
        "location_configured": False,
        "steps": steps,
    }
    return render(request, "website/find_us.html", context)
