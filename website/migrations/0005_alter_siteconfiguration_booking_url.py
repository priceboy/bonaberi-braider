# Update the admin label and setup guidance for WhatsApp click-to-chat booking.
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0004_remove_hairstyle_image_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="siteconfiguration",
            name="booking_url",
            field=models.URLField(
                blank=True,
                default="",
                help_text=(
                    "Use a WhatsApp click-to-chat URL, e.g. https://wa.me/237XXXXXXXXX "
                    "(international number, digits only; no +, spaces, or dashes). "
                    "Leave blank until the salon's number is confirmed."
                ),
                verbose_name="WhatsApp booking link",
            ),
        ),
    ]
