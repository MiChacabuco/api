from django import forms
from django.contrib.gis.geos import Point


class LatLongWidget(forms.MultiWidget):
    """
    A Widget that splits Point input into longitude/latitude text inputs.
    """

    def __init__(self, attrs=None):
        widgets = [forms.TextInput(attrs=attrs), forms.TextInput(attrs=attrs)]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if not value:
            return None, None
        return tuple(value.coords)

    def value_from_datadict(self, data, files, name):
        lon = data[name + "_0"]
        lat = data[name + "_1"]

        try:
            point = Point(float(lon), float(lat))
            return point
        except ValueError:
            return ""
