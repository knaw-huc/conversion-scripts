# -*- coding: utf-8 -*-
from location import Location

class Collective:
    prefix = ""
    object_name = ""
    url = ""
    collective = ""
    location = None
    items = {}

    def __init__(self, prefix, object_name="collective", url="", collective=""):
        self.prefix = prefix
        self.object_name = object_name
        self.url = url
        self.collective = collective
        self.items = {}

    def __str__(self):
        return self.collective

    def add_location(self, location):
        if type(location) is Location:
            self.location = location
        else:
            sys.stderr.write("Can't add object {} as location; should be \
Location\n".format(publisher.__class__))

    def add_item(self, item, value):
        if item == "location":
            self.add_location(value)
        elif item in self.items:
            self.items[item] += " " + value
        else:
            self.items[item] = value

    def rdfxml(self):
        result = ""
        result += '<{0}:{1} rdf:about="{2}">\n'.format(self.prefix,
                self.object_name, self.url)
        if self.collective:
            result += "  <{0}:displayName>{1}</{0}:displayName>\n".format(self.prefix,
                        self.collective)
        result += "  <schema:title>{1}</schema:title>\n".format(self.prefix,
                        self.collective)
        if self.location:
            result += '<{0}:{1} rdf:about="{2}">\n'.format(self.prefix,
                self.object_name, self.location.url)

            result += "  <{0}:location>{1}</{0}:location>\n".format(self.prefix,
                        self.location)
        for key in self.items:
            result += "  <{0}:{1}>{2}</{0}:{1}>\n".format(self.prefix,
                    key, self.items[key])
        result += '</{0}:{1}>\n'.format(self.prefix, self.object_name)
        if self.location:
            result += self.location.rdfxml()

        return result

