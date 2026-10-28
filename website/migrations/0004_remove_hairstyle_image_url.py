# Remove the temporary external-image field while preserving the already-published migration history.
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0003_siteconfiguration"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="hairstyle",
            name="image_url",
        ),
        migrations.AlterField(
            model_name="hairstyle",
            name="image",
            field=models.ImageField(
                blank=True,
                help_text="Upload genuine salon work. Transparent PNG/WebP recommended for Home cutouts.",
                null=True,
                upload_to="hairstyles/",
            ),
        ),
    ]
