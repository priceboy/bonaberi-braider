from urllib.parse import quote

from django.shortcuts import get_object_or_404, render

from .models import BusinessProfile, Hairstyle


def get_business():
    return BusinessProfile.objects.first()


def whatsapp_url(number, message):
    digits = "".join(ch for ch in number if ch.isdigit())
    return f"https://wa.me/{digits}?text={quote(message)}"


def home(request):
    business = get_business()
    context = {
        "business": business,
        "styles": list(Hairstyle.objects.filter(published=True)),
        "categories": ["Braids", "Locs", "Twists", "Wigs", "Natural Hair", "Other"],
        "whatsapp_chat": whatsapp_url(business.whatsapp_number, "Hi, I'd like to book an appointment.")
        if business
        else "",
    }
    return render(request, "studio/home.html", context)


def style_detail(request, slug):
    style = get_object_or_404(Hairstyle, slug=slug, published=True)
    business = get_business()
    context = {
        "business": business,
        "style": style,
        "whatsapp_chat": whatsapp_url(business.whatsapp_number, "Hi, I'd like to book an appointment.")
        if business
        else "",
        "whatsapp_book": whatsapp_url(business.whatsapp_number, f"Hi, I'd like to book the {style.title} hairstyle.")
        if business
        else "",
    }
    return render(request, "studio/style_detail.html", context)