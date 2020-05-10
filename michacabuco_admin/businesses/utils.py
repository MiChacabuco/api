import requests
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


def set_business_point(business: "Business"):
    """Calculate coordinates from business' address"""
    address = business.address
    if not address:
        # No address, clear point.
        business.point = None
        return
    url = "https://nominatim.openstreetmap.org/search"
    params = {"street": address, "postalcode": "6740", "format": "json"}
    try:
        response = requests.get(url, params, timeout=2)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        # Request failed, do nothing.
        return
    response_json = response.json()
    try:
        result = response_json[0]
        lon, lat = float(result["lon"]), float(result["lat"])
    except (IndexError, KeyError):
        # No results, do nothing.
        return
    business.point = Point(lon, lat)


def set_business_facebook(business: "Business"):
    """Convert FB URL to FB ID"""
    facebook = business.facebook
    if not "facebook.com" in facebook:
        # Not an URL, do nothing.
        return

    url = "https://findmyfbid.com"
    data = {"url": facebook}
    try:
        response = requests.post(url, data, timeout=2)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        # Request failed, do nothing.
        return
    response_json = response.json()
    try:
        id = response_json["id"]
    except (KeyError, TypeError):
        # No results, do nothing.
        return
    business.facebook = id
