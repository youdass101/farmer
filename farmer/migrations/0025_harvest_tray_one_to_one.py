from django.db import migrations, models
import django.db.models.deletion


def ensure_harvest_trays_are_unique(apps, schema_editor):
    Harvest = apps.get_model("farmer", "Harvest")
    duplicate = (
        Harvest.objects.values("tray_id")
        .annotate(count=models.Count("id"))
        .filter(count__gt=1)
        .order_by("tray_id")
        .first()
    )
    if duplicate:
        raise RuntimeError(
            "Cannot enforce one harvest per tray because tray "
            f"{duplicate['tray_id']} has {duplicate['count']} harvest records. "
            "Resolve duplicate harvest records before applying this migration."
        )


class Migration(migrations.Migration):
    dependencies = [
        ("farmer", "0024_plant_active"),
    ]

    operations = [
        migrations.RunPython(
            ensure_harvest_trays_are_unique,
            migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="harvest",
            name="tray",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to="farmer.tray",
            ),
        ),
    ]
