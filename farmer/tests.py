from datetime import date, timedelta
from unittest.mock import patch

from django.contrib.auth.models import AnonymousUser
from django.template.loader import render_to_string
from django.db import IntegrityError, transaction
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


class MediumViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="medium-editor", password="password")
        self.client.force_login(self.user)
        self.medium = Medium.objects.create(name="Soil", soil=100, coco=0)

    def test_edit_button_loads_medium_edit_form(self):
        response = self.client.post(
            reverse("medium"),
            {"type": "loadedit", "id": self.medium.id},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["editform"].instance, self.medium)
        self.assertContains(response, f'name="id" value="{self.medium.id}"')

    def test_medium_list_edit_button_submits_id(self):
        response = self.client.get(reverse("medium"))

        self.assertContains(response, f'name="id" value="{self.medium.id}" hidden')
        self.assertNotContains(response, 'name="itemid"')


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

    def test_bulk_harvest_can_harvest_part_of_available_group(self):
        available_trays = [self.create_tray(number) for number in range(3, 11)]
        all_trays = self.trays + available_trays

        response = self.client.post(
            reverse("harvest"),
            self.bulk_harvest_data(trays=all_trays, quantity=2),
        )

        self.assertRedirects(response, reverse("index"))
        bulk_harvest = BulkHarvest.objects.get()
        self.assertEqual(bulk_harvest.Trays, 2)
        self.assertSetEqual(
            set(Harvest.objects.values_list("tray_id", flat=True)),
            {self.trays[0].id, self.trays[1].id},
        )
        self.assertEqual(Harvest.objects.count(), 2)

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

    def test_bulk_harvest_rejects_quantity_greater_than_available_trays(self):
        response = self.client.post(
            reverse("harvest"),
            self.bulk_harvest_data(quantity=3),
        )

        self.assertEqual(response.status_code, 400)
        self.assertContains(
            response,
            "Tray quantity cannot exceed the number of available trays.",
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


class HarvestTrayInvariantTests(TestCase):
    def setUp(self):
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
        self.tray = Tray.objects.create(
            name=self.plant,
            number=1,
            medium=self.medium,
            start=timezone.now(),
            medium_weight=100,
            seeds_weight=10,
        )

    def test_database_rejects_second_harvest_for_same_tray(self):
        Harvest.objects.create(tray=self.tray, date=date(2026, 6, 8), output=100)

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Harvest.objects.create(
                    tray=self.tray,
                    date=date(2026, 6, 9),
                    output=120,
                )

        self.assertEqual(Harvest.objects.filter(tray=self.tray).count(), 1)

    def test_serialize_marks_tray_without_harvest_as_active(self):
        serialized = self.tray.serialize()

        self.assertFalse(serialized["harvest"])
        self.assertIsNone(serialized["harvest_id"])

    def test_serialize_returns_the_trays_single_harvest(self):
        harvest = Harvest.objects.create(
            tray=self.tray,
            date=date(2026, 6, 8),
            output=100,
        )

        serialized = self.tray.serialize()

        self.assertTrue(serialized["harvest"])
        self.assertEqual(serialized["harvest_id"], harvest.id)
        self.assertEqual(serialized["harvest_weight"], harvest.output)


class ReportViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="reporter", password="password")
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
        BulkHarvest.objects.create(
            Product=self.plant,
            MediumMix=self.medium,
            Trays=2,
            Harvestdate=date(2026, 6, 1),
            PacksQtt=0,
            MixWeight=100,
        )
        BulkHarvest.objects.create(
            Product=self.plant,
            MediumMix=self.medium,
            Trays=3,
            Harvestdate=date(2026, 6, 2),
            PacksQtt=0,
            MixWeight=150,
        )

    def report_data(self, **overrides):
        data = {
            "type": "Mix",
            "product": self.plant.id,
            "start_year": 2026,
            "start_month": 6,
            "start_day": 1,
            "end_year": 2026,
            "end_month": 6,
            "end_day": 30,
        }
        data.update(overrides)
        return data

    def test_product_mix_report_accumulates_all_matching_records(self):
        response = self.client.post(reverse("report"), self.report_data())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["totalyield"], 250)
        self.assertEqual(response.context["medium"], 500)
        self.assertEqual(len(response.context["data"]), 2)

    def test_invalid_report_form_returns_errors_without_crashing(self):
        response = self.client.post(reverse("report"), {"type": "Mix"})

        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.context["fform"].errors)
        self.assertEqual(response.context["data"], [])


class ExceptionHandlingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="farmer-errors", password="password")
        self.client.force_login(self.user)

    def test_malformed_plant_json_returns_bad_request(self):
        response = self.client.post(
            reverse("plants"),
            data="not-json",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {"error": "Invalid JSON payload."})
