from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0008_attach_direction_steps_to_site_configuration"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hairstyle",
            name="is_demo",
            field=models.BooleanField(
                default=False,
                help_text="Demo entries use stock photos. Uploading a real image automatically clears this flag.",
            ),
        ),
    ]
