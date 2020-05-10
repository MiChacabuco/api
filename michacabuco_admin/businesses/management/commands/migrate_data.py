import imghdr
import json
import os
import re
from itertools import chain

from django.contrib.gis.geos import Point
from django.core.files import File
from django.core.management import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from michacabuco_admin.businesses.models import Tag, Business, BusinessPhone


def create_tags(*values):
    tags = []
    for value in values:
        tag, _ = Tag.objects.get_or_create(value=value)
        tags.append(tag)
    return tags


pharmacy_category_id = "5e4fea87df27824c74a43255"
category_tags_map = {
    pharmacy_category_id: create_tags("farmacias", "medicamentos"),
    "5e0ccf5876d7ff5cae9ad4f3": create_tags("lavanderías", "ropa"),
    "5e2908b834357cd1aabba6da": create_tags("heladerías", "helados"),
    "5e0f4dccac324f791f21fe36": create_tags("abogados"),
    "5e297246b2a21dbf2b27b1c9": create_tags("pizzerías", "pizzas"),
    "5e318a53d88970f6bbce9ba6": create_tags("artesanías", "manualidades"),
    "5e318d1be04dc72e5cb93e54": create_tags(
        "reposterías", "tortas", "postres", "dulces"
    ),
    "5e2a012f3bce239d2e44c140": create_tags("cervecerías", "cervezas"),
    "5e2b7e837873c536855e3bea": create_tags("remiserías", "remises", "taxis"),
    "5de8350e3cf0ce8a41288bdc": create_tags("comunicación"),
    "5e2f5a463f983dcf0f768767": create_tags("contadores"),
    "5e2f4f2cef0f6b1f959a09ab": create_tags(
        "indumentaria", "ropa", "masculinas", "hombres"
    ),
    "5e2f64ef244325bf38ce1b84": create_tags(
        "indumentaria", "ropa", "femeninas", "mujeres"
    ),
    "5e321293bf7e366672930f10": create_tags(
        "indumentaria", "ropa", "infantil", "nenes", "bebés"
    ),
    "5e9a3a83c2c395c8e223567b": create_tags(
        "indumentaria",
        "ropa",
        "unisex",
        "masculinas",
        "hombres",
        "femeninas",
        "mujeres",
    ),
    "5e34a354bf7e366672930f22": create_tags("indumentaria", "ropa", "deportiva"),
    "5e13e3e76e39e66132425c12": create_tags("psicopedagogos", "psicopedagogas"),
    "5e584df32ca27a8a578222a7": create_tags(
        "boliches", "fiesta", "música", "bar", "discoteca"
    ),
    "5e15062e247d7eca761db86e": create_tags("agencia", "viajes"),
    "5e35692fbbaa08a7bf7244d1": create_tags("kinesiólogos", "kinesiología"),
    "5e356cb4e04dc72e5cb93e61": create_tags("cardiólogos"),
    "5e337da2b3d3eaf1afe26b4e": create_tags("ecológicos", "sustentables"),
    "5e356d04ef0f6b1f959a09c1": create_tags("nefrólogos", "riñones"),
    "5e5d81b1802d1a453ce9509f": create_tags("jugos", "licuados", "batidos"),
    "5e683633972a08f8c44d83cc": create_tags(
        "inmobiliarias", "alquileres", "casas", "departamentos"
    ),
    "5e356e1b41216d4219d96253": create_tags("neurocirujanos"),
    "5e357752d88970f6bbce9bb6": create_tags("ginecólogos"),
    "5e39db4216700e8a9756141e": create_tags("librerías"),
    "5e340ae441216d4219d9624f": create_tags("mecánicos", "autos"),
    "5e342d2db3d3eaf1afe26b52": create_tags("asesores", "imagen"),
    "5e3ab39eb791af625d26114b": create_tags("papelerías"),
    "5e553c332ca27a8a578222a0": create_tags("peluquerías", "femeninas", "mujeres"),
    "5e3ae55216700e8a97561421": create_tags(
        "peluquerías", "unisex", "femeninas", "mujeres", "masculinas", "hombres"
    ),
    "5e3b7ca9b791af625d26114d": create_tags("ferreterías"),
    "5e3eac5354597bdd2e4e49d3": create_tags("cacerolas", "essen"),
    "5e3eb511b66062e0b5c6f9ce": create_tags(
        "distribuidoras", "mayoristas", "alimentos", "bebidas"
    ),
    "5e0cbe7476d7ff5cae9ad4f1": create_tags(
        "desarrolladores", "programadores", "páginas", "web"
    ),
    "5e0cc20976d7ff5cae9ad4f2": create_tags("mascotas", "animales"),
    "5e5718892ca27a8a578222a6": create_tags(
        "forrajerías", "animales", "mascotas", "alimento balanceado"
    ),
    "5e3eb78516700e8a97561423": create_tags("cirujanos"),
    "5e378a98ec911fc00b300cde": create_tags("fonoaudiólogos"),
    "5e378b689bcbf52c7c8a2a06": create_tags("endocrinólogos"),
    "5e338b30ef0f6b1f959a09bc": create_tags("seguros", "aseguradoras"),
    "5e39efa891cd47f43473a726": create_tags("nutricionistas", "dieta"),
    "5e40040d16700e8a97561424": create_tags(
        "estación", "servicio", "nafta", "gasoil", "combustibles"
    ),
    "5e4001d0b791af625d261152": create_tags("rotiserías", "comida"),
    "5e42eab57dea68f87ed2a9b9": create_tags("fotógrafos", "fotos"),
    "5e42ed94fdd14979df9d0f2f": create_tags("cotillones"),
    "5e2f7f02e04dc72e5cb93e4c": create_tags("seguridad e higiene"),
    "5e3eba7e9bcbf52c7c8a2a10": create_tags(
        "seguridad", "alarmas", "monitoreo", "vigilancia"
    ),
    "5e4b1c7f2ca27a8a57822268": create_tags("veterinarias", "animales", "mascotas"),
    "5e4b6935df27824c74a43240": create_tags("cerrajerías", "cerrajero", "llaves"),
    "5e4bdac4df27824c74a43244": create_tags(
        "granjas", "pollos", "pollerías", "pollajerías"
    ),
    "5e3497f3244325bf38ce1b97": create_tags("celulares", "teléfonos"),
    "5e377d2491cd47f43473a723": create_tags("informática", "computadoras", "notebooks"),
    "5e4879b02ca27a8a5782225b": create_tags("masajistas", "masajes"),
    "5e472db77dea68f87ed2a9bb": create_tags("herrerías"),
    "5e4b05a9df27824c74a43236": create_tags("pescaderías", "pescados", "mariscos"),
    "5e4a99677dea68f87ed2a9c1": create_tags(
        "carnicerías", "carnes", "asado", "chorizos", "embutidos"
    ),
    "5e4aa7eedf27824c74a43233": create_tags(
        "chacinados",
        "chancherías",
        "carnes",
        "cerdos",
        "chanchos",
        "chorizos",
        "embutidos",
    ),
    "5e321526244325bf38ce1b8b": create_tags("diseñadores", "gráficos"),
    "5e224ae42e9d7da63405635a": create_tags(
        "restobar", "restaurante", "bar", "cerveza"
    ),
    "5e2a6d4eb1775a112181ccaa": create_tags(
        "confiterías", "cafés", "desayunos", "meriendas"
    ),
    "5e23aa4be02fb94d3d9f389e": create_tags(
        "confiterías", "cafés", "desayunos", "meriendas"
    ),
    "5e2a66b9b1775a112181cca9": create_tags(
        "comida", "rápida", "fastfood", "hamburgueserías", "hamburguesas"
    ),
    "5e2a1f5409475fa9d9c7c03d": create_tags("restaurante"),
    "5e30196bd88970f6bbce9ba4": create_tags("electricistas"),
    "5e30ea7c3f983dcf0f768773": create_tags("desayunos"),
    "5e34083e3f983dcf0f76877b": create_tags("neurólogos"),
    "5e342239ef0f6b1f959a09be": create_tags("supermercados"),
    "5e348b92bbaa08a7bf7244cc": create_tags("lencerías", "ropa íntima"),
    "5e51a0362ca27a8a57822291": create_tags("empanaderías", "empanadas"),
    "5e51a6fe7dea68f87ed2a9fe": create_tags("zapaterías", "zapatos", "zapatillas"),
    "5e50029e7dea68f87ed2a9f2": create_tags("pinturerías", "pinturas"),
    "5e4ff3802ca27a8a5782228a": create_tags("joyerías", "joyas", "relojes", "anillos"),
    "5e301640ef0f6b1f959a09ad": create_tags("accesorios", "bijouteries"),
    "5e349ab741216d4219d96252": create_tags("gimnasios", "gym"),
    "5e339bbc41216d4219d9624c": create_tags("blanquerías", "hogar"),
    "5e321c8abf7e366672930f12": create_tags("psicólogos", "psicólogas"),
    "5e33992241216d4219d9624b": create_tags("odontólogos", "dentistas"),
    "5e337f633f983dcf0f768778": create_tags(
        "verdulerías", "fruterías", "verduras", "frutas", "frutihortícolas"
    ),
    "5e3357e341216d4219d96246": create_tags("kioscos", "quioscos"),
    "5e2f61eabbaa08a7bf7244b8": create_tags("comisionistas", "comisiones"),
    "5e30f615e04dc72e5cb93e53": create_tags("ingeniero electrónico"),
    "5e2f8156e04dc72e5cb93e4d": create_tags("regalerías", "regalos"),
    "5e2fb5f13f983dcf0f76876b": create_tags("panaderías", "pan", "facturas"),
    "5e30c5eeef0f6b1f959a09b0": create_tags("enfermeros", "enfermeras"),
    "5e30e55aef0f6b1f959a09b1": create_tags("profesores", "inglés"),
    "5e320d35e04dc72e5cb93e55": create_tags("construcción", "materiales", "obras"),
    "5e3218c4244325bf38ce1b8c": create_tags("estética", "belleza"),
    "5e32484cb3d3eaf1afe26b4a": create_tags("comida"),
    "5e324d8c41216d4219d96243": create_tags("eventos", "cumpleaños"),
    "5de834e03cf0ce8a41288bd8": create_tags("bancos", "cajeros"),
    "5de82d3a3cf0ce8a41288bd2": create_tags("emergencias"),
    "5de82d543cf0ce8a41288bd3": create_tags("policía"),
    "5de82d9b3cf0ce8a41288bd4": create_tags("salud"),
    "5de834e73cf0ce8a41288bd9": create_tags("transporte", "colectivos"),
    "5de835043cf0ce8a41288bdb": create_tags("obra social", "obras sociales"),
}


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
        files_to_close = []

        for business_dict in data:
            if business_dict["type"] == "pharmacy":
                # Skip pharmacies
                continue

            name = business_dict["name"]
            print(f"Processing business: {name}")
            kwargs = {
                "name": name,
                "summary": business_dict.get("summary", ""),
                "address": business_dict.get("address", ""),
                "instagram": business_dict.get("instagram", ""),
                "facebook": business_dict.get("facebook", ""),
                "email": business_dict.get("email", ""),
                "website": business_dict.get("website", ""),
                "has_delivery": business_dict.get("hasDelivery", False),
                "is_useful": business_dict["type"] == "organization"
                and business_dict["category"] != pharmacy_category_id,
                "is_visible": True,
            }
            # Avatar
            avatar = business_dict.get("avatar")
            if avatar:
                avatar_path = os.path.join("avatars", avatar["$oid"])
                avatar_file = open(avatar_path, "rb")
                avatar_format = imghdr.what(avatar_path)
                avatar_name = f"{slugify(name)}.{avatar_format}"
                kwargs["avatar"] = File(avatar_file, avatar_name)
                files_to_close.append(avatar_file)
            try:
                coordinates = business_dict["location"]["coordinates"]
                kwargs["point"] = Point(*coordinates)
            except TypeError:
                # It's a list, not an object
                coordinates = business_dict["location"]
                kwargs["point"] = Point(*coordinates)
            except KeyError:
                # No coordinates, do nothing.
                pass

            business = Business(**kwargs)
            businesses_batch.append(business)
            business_phones = []

            # Whatsapp
            try:
                whatsapp = business_dict["whatsapp"]
                # Format it like "(02352) 15-123456"
                whatsapp = re.sub(
                    r"(?:\+549)(2352|236|221|11|3585)(.*)", r"(0\1) 15-\2", whatsapp
                )
                business_phones.append(BusinessPhone(number=whatsapp, is_whatsapp=True))
            except KeyError:
                whatsapp = None
                # No WhatsApp number, do nothing.
                pass

            # Phones
            for number in business_dict.get("phones", []):
                if number == whatsapp:
                    # Skip number if already added as WhatsApp
                    continue
                business_phones.append(BusinessPhone(number=number, is_whatsapp=False))
            phones_batch.append(business_phones)
            businesses_dict.append(business_dict)

        # Transactional insert
        BusinessTag = Business.tags.through
        with transaction.atomic():
            # Bulk insert businesses
            print("Creating businesses ...")
            businesses_batch = Business.objects.bulk_create(businesses_batch)

            tags_batch = []
            for i, business in enumerate(businesses_batch):
                # Link tags
                try:
                    category_id = businesses_dict[i]["category"]["$oid"]
                    tags = category_tags_map.get(category_id, [])
                    for tag in tags:
                        tags_batch.append(BusinessTag(business=business, tag=tag))
                except KeyError:
                    pass

                # Link phones
                business_phones = phones_batch[i]
                for phone in business_phones:
                    phone.business = business

            print("Creating phones ...")
            # Flatten and bulk insert phones
            phones_batch = chain.from_iterable(phones_batch)
            BusinessPhone.objects.bulk_create(phones_batch)

            # Bulk insert tags
            print("Creating tags ...")
            BusinessTag.objects.bulk_create(tags_batch)

        # Close every file
        for file in files_to_close:
            file.close()
        print(f"DONE. {len(businesses_batch)} businesses inserted.")
