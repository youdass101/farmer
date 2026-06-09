from datetime import date, timedelta
from unittest.mock import patch

from django.contrib.auth.models import AnonymousUser
from django.template.loader import render_to_string
from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.utils import timezone

from .dfunctions.bulkharvest import parse_tray_ids
from .models import BulkHarvest, Harvest, Medium, Plant, Tray, User


class TrayListTemplateTests(SimpleTestCase):
    def test_tray_actions_post_to_traylist_view(self):
        tray = {
            "id": 1,
            "name": "Pea",
            "number": 1,
            "days": timedelta(days=2),
            "medium_weight": 100,
            "seeds_weight": 20,
            "medium": "Soil",
            "start": date(2026, 6, 1),
            "end": date(2026, 6, 8),
        }

        html = render_to_string(
            "farmer/traylist.html",
            {
                "user": AnonymousUser(),
                "form": "",
                "data": [tray],
                "harvestform": "",
            },
        )

        traylist_action = f'action="{reverse("traylist")}"'
        self.assertEqual(html.count(traylist_action), 4)
        self.assertNotIn('action="/"', html)
        self.assertIn(f'action="{reverse("harvest")}"', html)


class BulkHarvestHelperTests(SimpleTestCase):
    def test_parse_tray_ids_returns_unique_integer_ids(self):
        self.assertEqual(parse_tray_ids("[1, '2']"), [1, 2])

    def test_parse_tray_ids_rejects_empty_or_duplicate_ids(self):
        with self.assertRaisesMessage(ValueError, "Select at least one valid tray"):
            parse_tray_ids("[]")

        with self.assertRaisesMessage(ValueError, "cannot be selected more than once"):
            parse_tray_ids("[1, 1]")


class BulkHarvestViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="farmer", password="password")
        self.client.force_login(self.user)
        self.plant = Plant.objects.create(
            name="Pea",
            seeds=10,
            pressure=1,
            blackout=1,
            harvest=7,
            medium_weight=100,
            packweight=50,
        )
        self.medium = Medium.objects.create(name="Soil", soil=100, coco=0)
        self.trays = [self.create_tray(1), self.create_tray(2)]

    def create_tray(self, number, plant=None, medium=None):
        return Tray.objects.create(
            name=plant or self.plant,
            number=number,
            medium=medium or self.medium,
            start=timezone.now(),
            medium_weight=100,
            seeds_weight=10,
        )

    def bulk_harvest_data(self, trays=None, quantity=None, **overrides):
        trays = trays or self.trays
        data = {
            "type": "bulknew",
            "id": str([tray.id for tray in trays]),
            "Trays": quantity if quantity is not None else len(trays),
            "PacksQtt": 1,
            "MixWeight": 50,
            "Harvestdate_year": 2026,
            "Harvestdate_month": 6,
            "Harvestdate_day": 7,
        }
        data.update(overrides)
        return data

    def test_bulk_harvest_creates_all_records(self):
        response = self.client.post(reverse("harvest"), self.bulk_harvest_data())

        self.assertRedirects(response, reverse("index"))
        self.assertEqual(BulkHarvest.objects.count(), 1)
        self.assertEqual(Harvest.objects.count(), 2)
        self.assertSetEqual(
            set(Harvest.objects.values_list("tray_id", flat=True)),
            {tray.id for tray in self.trays},
        )

    def test_invalid_bulk_harvest_form_returns_errors_without_writes(self):
        response = self.client.post(
            reverse("harvest"),
            self.bulk_harvest_data(PacksQtt="", MixWeight=""),
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(BulkHarvest.objects.count(), 0)
        self.assertEqual(Harvest.objects.count(), 0)

    def test_bulk_harvest_rejects_zero_output_without_writes(self):
        response = self.client.post(
            reverse("harvest"),
            self.bulk_harvest_data(PacksQtt=0, MixWeight=0),
        )

        self.assertEqual(response.status_code, 400)
        self.assertContains(
            response,
            "Harvest output must be greater than zero.",
            status_code=400,
        )
        self.assertEqual(BulkHarvest.objects.count(), 0)
        self.assertEqual(Harvest.objects.count(), 0)

    def test_bulk_harvest_rejects_quantity_mismatch(self):
        response = self.client.post(
            reverse("harvest"),
            self.bulk_harvest_data(quantity=3),
        )

        self.assertEqual(response.status_code, 400)
        self.assertContains(
            response,
            "Tray quantity must match the number of selected trays.",
            status_code=400,
        )
        self.assertContains(response, 'style="display: block;"', status_code=400)
        self.assertEqual(
            response.context["bulk_tray_ids"],
            str([tray.id for tray in self.trays]),
        )
        self.assertEqual(BulkHarvest.objects.count(), 0)
        self.assertEqual(Harvest.objects.count(), 0)

    def test_bulk_harvest_rejects_mixed_products(self):
        other_plant = Plant.objects.create(
            name="Radish",
            seeds=10,
            pressure=1,
            blackout=1,
            harvest=7,
            medium_weight=100,
            packweight=50,
        )
        mixed_tray = self.create_tray(1, plant=other_plant)

        response = self.client.post(
            reverse("harvest"),
            self.bulk_harvest_data(trays=[self.trays[0], mixed_tray]),
        )

        self.assertEqual(response.status_code, 400)
        self.assertContains(
            response,
            "All selected trays must use the same product and medium.",
            status_code=400,
        )
        self.assertEqual(BulkHarvest.objects.count(), 0)
        self.assertEqual(Harvest.objects.count(), 0)

    def test_bulk_harvest_rolls_back_when_harvest_creation_fails(self):
        with patch.object(Harvest.objects, "bulk_create", side_effect=RuntimeError):
            with self.assertRaises(RuntimeError):
                self.client.post(reverse("harvest"), self.bulk_harvest_data())

        self.assertEqual(BulkHarvest.objects.count(), 0)
        self.assertEqual(Harvest.objects.count(), 0)
