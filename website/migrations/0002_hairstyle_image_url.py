# Generated for the canonical website hairstyle image field.
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hairstyle",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="hairstyles/"),
        ),
        migrations.AddField(
            model_name="hairstyle",
            name="image_url",
            field=models.URLField(
                blank=True,
                default="",
                help_text="Optional external image URL. Uploaded images take precedence.",
            ),
        ),
    ]
