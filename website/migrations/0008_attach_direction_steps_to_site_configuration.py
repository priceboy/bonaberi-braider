from django.db import migrations, models
import django.db.models.deletion


def attach_existing_steps(apps, schema_editor):
    SiteConfiguration = apps.get_model("website", "SiteConfiguration")
    DirectionStep = apps.get_model("website", "DirectionStep")

    config = SiteConfiguration.objects.order_by("pk").first()
    if config is None:
        config = SiteConfiguration.objects.create()
    DirectionStep.objects.filter(site_configuration__isnull=True).update(
        site_configuration_id=config.pk
    )


class Migration(migrations.Migration):
    dependencies = [("website", "0007_seed_demo_hairstyles")]

    operations = [
        migrations.AddField(
            model_name="directionstep",
            name="site_configuration",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="direction_steps",
                to="website.siteconfiguration",
            ),
        ),
        migrations.RunPython(attach_existing_steps, migrations.RunPython.noop),
    ]
