from django.db import migrations, models


BOOKING_URL = "https://wa.me/237672748984"


def populate_booking_url(apps, schema_editor):
    SiteConfiguration = apps.get_model("website", "SiteConfiguration")
    SiteConfiguration.objects.filter(booking_url="").update(booking_url=BOOKING_URL)


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0005_alter_siteconfiguration_booking_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="siteconfiguration",
            name="booking_url",
            field=models.URLField(
                blank=True,
                default=BOOKING_URL,
                help_text=(
                    "WhatsApp click-to-chat link. The current configured number is "
                    "+237 672 74 89 84. Update this URL if the salon changes its booking number."
                ),
                verbose_name="WhatsApp booking link",
            ),
        ),
        migrations.RunPython(populate_booking_url, migrations.RunPython.noop),
    ]
