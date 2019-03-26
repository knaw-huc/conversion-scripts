# -*- coding: utf-8 -*-


class Location:
    prefix = ""
    url = ""
    object_name = ""
    location = ""
    longitude = ""
    latitude = ""
    items = {}

    def __init__(self, prefix, object_name="location", url="", location=""):
        self.prefix = prefix
        self.object_name = object_name
        self.url = url
        self.location = location
        self.items = {}

    def set_latitude(self, lat):
        self.latitude = lat

    def set_longitude(self, long):
        self.longitude = long

    def add_item(self, item, value):
        if item in self.items:
            self.items[item] += " " + value
        else:
            self.items[item] = value

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
        for key in self.items:
            result += "  <{0}:{1}>{2}</{0}:{1}>\n".format(self.prefix,
                    key, self.items[key])
        result += '</{0}:{1}>\n'.format(self.prefix, self.object_name)
        return result

