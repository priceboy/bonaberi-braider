# Generated for the editable public-site configuration.
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0002_hairstyle_image_url"),
    ]

    operations = [
        migrations.CreateModel(
            name="SiteConfiguration",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("salon_name", models.CharField(blank=True, default="", max_length=120)),
                ("tagline", models.CharField(blank=True, default="", max_length=200)),
                ("hero_title", models.CharField(blank=True, default="", max_length=160)),
                ("hero_text", models.CharField(blank=True, default="", max_length=400)),
                ("home_background", models.ImageField(blank=True, help_text="Salon interior photo used behind the Home page content.", null=True, upload_to="site/")),
                ("booking_url", models.URLField(blank=True, default="", help_text="Real booking/contact destination. Leave blank until confirmed.")),
                ("address", models.CharField(blank=True, default="", max_length=250)),
                ("map_embed_url", models.URLField(blank=True, default="", help_text="Optional map embed URL supplied by the owner.")),
                ("map_open_url", models.URLField(blank=True, default="", help_text="Optional public Google Maps or map-app destination.")),
            ],
            options={
                "verbose_name": "Site configuration",
                "verbose_name_plural": "Site configuration",
            },
        ),
    ]
