# -*- coding: utf-8 -*-


class Location:
    prefix = ""
    url = ""
    object_name = ""
    location = ""
    longitude = ""
    latitude = ""

    def __init__(self, prefix, object_name="location", url="", location=""):
        self.prefix = prefix
        self.object_name = object_name
        self.url = url
        self.location = location

    def set_latitude(self, lat):
        self.latitude = lat

    def set_longitude(self, long):
        self.longitude = long

    def __str__(self):
        return self.location

    def all_data(self):
        coordinates = ""
        if self.latitude:
            coordinates += " ({}, ".format(self.latitude)
        if self.longitude:
            coordinates += "{})".format(self.longitude)
        return "{0}{1}".format(self.location, coordinates)

    def rdfxml(self):
        result = ""
        result += '<{0}:{1} rdf:about="{2}">\n'.format(self.prefix, self.object_name,
                self.url)
        if self.location:
            result += " <{0}:displayName>{1}</{0}:displayName>\n".format(self.prefix,
                    self.location)
        if self.latitude:
            result += "  <{0}:latitude>{1}</{0}:latitude>\n".format(self.prefix,
                    self.latitude)
        if self.longitude:
            result += "  <{0}:longitude>{1}</{0}:longitude>\n".format(self.prefix,
                    self.longitude)
        result += "  <schema:title>{0}</schema:title>\n".format(self)
        result += '</{0}:{1}>\n'.format(self.prefix, self.object_name)
        return result

