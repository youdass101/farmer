import ast

from django.db import transaction

from ..forms import Nbulkharvest
from ..models import Harvest, Tray


class BulkHarvestValidationError(Exception):
    """Carries a bound bulk-harvest form back to the view for rendering."""

    def __init__(self, form, message=None):
        if message:
            form.add_error(None, message)
        self.form = form
        super().__init__(message or "Invalid bulk harvest submission.")


def parse_tray_ids(raw_tray_ids):
    """Return a non-empty list of unique integer tray IDs."""
    try:
        tray_ids = ast.literal_eval(raw_tray_ids)
        if not isinstance(tray_ids, (list, tuple)) or not tray_ids:
            raise ValueError
        tray_ids = [int(tray_id) for tray_id in tray_ids]
    except (SyntaxError, TypeError, ValueError) as error:
        raise ValueError("Select at least one valid tray to harvest.") from error

    if len(tray_ids) != len(set(tray_ids)):
        raise ValueError("A tray cannot be selected more than once.")

    return tray_ids


def get_locked_trays(tray_ids):
    """Lock and return selected trays in the order supplied by the client."""
    trays_by_id = {
        tray.id: tray
        for tray in Tray.objects.select_for_update()
        .select_related("name", "medium")
        .filter(id__in=tray_ids)
    }

    if len(trays_by_id) != len(tray_ids):
        raise ValueError("One or more selected trays no longer exist.")

    return [trays_by_id[tray_id] for tray_id in tray_ids]


def build_bulk_harvest_form(form_data, trays):
    """Bind server-controlled product and medium values to the submitted form."""
    first_tray = trays[0]
    form_data.update({
        "Product": first_tray.name_id,
        "MediumMix": first_tray.medium_id,
    })
    return Nbulkharvest(form_data)


def select_trays_for_harvest(form, available_trays):
    """Select the requested number of trays from the available tray group."""
    tray_quantity = form.cleaned_data["Trays"]
    if tray_quantity > len(available_trays):
        form.add_error(
            "Trays",
            "Tray quantity cannot exceed the number of available trays.",
        )
        raise BulkHarvestValidationError(form)

    return available_trays[:tray_quantity]


def validate_selected_trays(form, trays):
    """Validate the trays selected for this harvest as one group."""
    first_tray = trays[0]
    if any(
        tray.name_id != first_tray.name_id
        or tray.medium_id != first_tray.medium_id
        for tray in trays
    ):
        form.add_error(
            None,
            "All selected trays must use the same product and medium.",
        )

    if Harvest.objects.filter(tray_id__in=[tray.id for tray in trays]).exists():
        form.add_error(
            None,
            "One or more selected trays have already been harvested.",
        )

    if form.errors:
        raise BulkHarvestValidationError(form)


def save_bulk_harvest(form, trays):
    """Create a bulk harvest and all per-tray harvest records."""
    bulk_harvest = form.save()
    output_per_tray = (
        bulk_harvest.PacksWeight + bulk_harvest.MixWeight
    ) / len(trays)
    Harvest.objects.bulk_create([
        Harvest(
            tray=tray,
            date=bulk_harvest.Harvestdate,
            output=output_per_tray,
            bulkh=bulk_harvest,
        )
        for tray in trays
    ])
    return bulk_harvest


def create_bulk_harvest(form_data):
    """Validate and atomically create a bulk harvest from submitted form data."""
    try:
        tray_ids = parse_tray_ids(form_data.get("id", ""))
    except ValueError as error:
        raise BulkHarvestValidationError(Nbulkharvest(form_data), str(error)) from error

    with transaction.atomic():
        try:
            trays = get_locked_trays(tray_ids)
        except ValueError as error:
            raise BulkHarvestValidationError(
                Nbulkharvest(form_data),
                str(error),
            ) from error

        form = build_bulk_harvest_form(form_data, trays)
        if not form.is_valid():
            raise BulkHarvestValidationError(form)

        selected_trays = select_trays_for_harvest(form, trays)
        validate_selected_trays(form, selected_trays)
        return save_bulk_harvest(form, selected_trays)
