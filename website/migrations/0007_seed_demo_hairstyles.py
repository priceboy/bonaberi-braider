from django.db import migrations, models
from django.utils.text import slugify

DEMO_STYLES = [
    ("Sculpted Knotless Braids", "Braids", "photo-1522337360788-8b13dee7a37e", True, 1),
    ("Soft Glam Waves", "Wigs", "photo-1512496015851-a90fb38ba796", True, 2),
    ("Crown Loc Style", "Locs", "photo-1549236177-f9b00317542b", True, 3),
    ("Defined Natural Curls", "Natural Hair", "photo-1525507119028-ed4c629a60a3", True, 4),
    ("Signature Senegalese Twists", "Twists", "photo-1508182311256-e3f7d0e5f1e2", True, 5),
    ("Editorial Occasion Style", "Occasion Styles", "photo-1487412720507-e7ab37603c6f", True, 6),
]


def seed_demo_styles(apps, schema_editor):
    Category = apps.get_model("website", "Category")
    Hairstyle = apps.get_model("website", "Hairstyle")
    for title, category_name, image_id, show_home, order in DEMO_STYLES:
        category, _ = Category.objects.get_or_create(
            name=category_name, defaults={"slug": slugify(category_name)}
        )
        Hairstyle.objects.get_or_create(
            title=title,
            category=category,
            defaults={
                "description": "Temporary demo listing. Replace this stock photo with the salon's own work.",
                "image_url": f"https://images.unsplash.com/{image_id}?auto=format&fit=crop&w=1400&q=85",
                "is_demo": True,
                "show_on_home": show_home,
                "show_in_carousel": True,
                "is_active": True,
                "sort_order": order,
            },
        )


def remove_demo_styles(apps, schema_editor):
    Hairstyle = apps.get_model("website", "Hairstyle")
    Hairstyle.objects.filter(is_demo=True).delete()


class Migration(migrations.Migration):
    dependencies = [("website", "0006_configure_whatsapp_booking")]
    operations = [
        migrations.AddField(
            model_name="hairstyle", name="image_url",
            field=models.URLField(blank=True, default="", help_text="Optional remote demo photo. An uploaded image takes priority."),
        ),
        migrations.AddField(
            model_name="hairstyle", name="is_demo",
            field=models.BooleanField(default=False, help_text="Demo entries use stock photos. Uncheck this when replacing with real salon work."),
        ),
        migrations.RunPython(seed_demo_styles, remove_demo_styles),
    ]
