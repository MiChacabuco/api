import json
from itertools import chain

from django.contrib.gis.geos import Point
from django.core.management import BaseCommand
from django.db import transaction

from michacabuco_admin.businesses.models import Business, BusinessPhone


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("json_file")

    def handle(self, *args, **options):
        # Open JSON
        json_file = options["json_file"]
        with open(json_file) as data_file:
            data = json.load(data_file)

        # Arrange businesses, phones and tags.
        businesses_batch = []
        phones_batch = []
        businesses_dict = []

        for business_dict in data:
            name = business_dict["commerce"]
            print(f"Processing business: {name}")
            kwargs = {
                "name": name.title(),
                "summary": business_dict["bio"],
                "address": business_dict["street"],
                "instagram": business_dict["linkinsta"],
                "facebook": business_dict["linkface"],
                "website": business_dict["linkweb"],
                "has_delivery": business_dict["delivery"] == "true",
                "is_visible": False,
            }
            coordinates = business_dict["coords"].split(", ")
            try:
                kwargs["point"] = Point(float(coordinates[1]), float(coordinates[0]))
            except IndexError:
                pass

            business = Business(**kwargs)
            businesses_batch.append(business)

            # Phones
            business_phones = []
            phone = business_dict["telephone"]
            if phone:
                business_phones.append(BusinessPhone(number=phone, is_whatsapp=False))
            cellphone = business_dict["cellphone"]
            if cellphone:
                is_whatsapp = business_dict["whatsapp"] == "true"
                business_phones.append(
                    BusinessPhone(number=cellphone, is_whatsapp=is_whatsapp)
                )
            phones_batch.append(business_phones)
            businesses_dict.append(business_dict)

        # Transactional insert
        with transaction.atomic():
            # Bulk insert businesses
            print("Creating businesses ...")
            businesses_batch = Business.objects.bulk_create(businesses_batch)

            for i, business in enumerate(businesses_batch):
                # Link phones
                business_phones = phones_batch[i]
                for phone in business_phones:
                    phone.business = business

            print("Creating phones ...")
            # Flatten and bulk insert phones
            phones_batch = chain.from_iterable(phones_batch)
            BusinessPhone.objects.bulk_create(phones_batch)

        print(f"DONE. {len(businesses_batch)} businesses inserted.")
