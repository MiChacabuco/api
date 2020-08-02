from json import JSONDecodeError

import requests
from celery import shared_task
from django.contrib.gis.geos import Point


@shared_task
def set_business_point(business_id, address: str):
    """Calculate coordinates from business' address"""
    from michacabuco_admin.businesses.models import Business

    url = "https://nominatim.openstreetmap.org/search"
    params = {"street": address, "postalcode": "6740", "format": "json"}
    try:
        response = requests.get(url, params, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        # Request failed, do nothing.
        return
    try:
        response_json = response.json()
        result = response_json[0]
        lon, lat = float(result["lon"]), float(result["lat"])
    except (IndexError, KeyError, JSONDecodeError):
        # No results, do nothing.
        return
    Business.objects.filter(id=business_id).update(point=Point(lon, lat))


@shared_task
def set_business_facebook(business_id, facebook: str):
    """Convert FB URL/username to FB ID"""
    from michacabuco_admin.businesses.models import Business

    if not "facebook.com" in facebook:
        # Not an URL
        try:
            int(facebook)
            # Already a FB ID, do nothing.
            return
        except ValueError:
            # Convert username to URL
            facebook = f"www.facebook.com/{facebook}"

    url = "https://fb-search.com/facebook-id"
    data = {"query": facebook}
    try:
        response = requests.post(url, data, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        # Request failed, do nothing.
        return
    try:
        response_json = response.json()
        facebook_id = response_json["id"]
    except (KeyError, TypeError, JSONDecodeError):
        # No results, do nothing.
        return
    Business.objects.filter(id=business_id).update(facebook=facebook_id)
