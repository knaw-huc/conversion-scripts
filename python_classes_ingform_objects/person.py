# -*- coding: utf-8 -*-
import re
from pnvperson import PnvPerson


class Person(PnvPerson):
    prefix = ""
    object_name = ""
    url = ""
    items = {}

    def __init__(self, prefix, object_name="person", url=""):
        PnvPerson.__init__(self)
        self.prefix = prefix
        self.object_name = object_name
        self.url = url
        self.items = {}
    
    def add_item(self, item, value):
        if item in self.items:
            self.items[item] += " " + value
        else:
            self.items[item] = value

    def rdfxml(self):
        name = PnvPerson.to_h(self)
        result = ""
        result += '<{0}:{1} rdf:about="{2}">\n'.format(self.prefix,
                self.object_name, self.url)
        result += "  <{0}:name>\n".format(self.prefix)
        for key in name.keys():
            value = name[key].strip()
            if value:
                result += "    <pnv:{0}>{1}</pnv:{0}>\n".format(key, value)
        result += "  </{0}:name>\n".format(self.prefix)
        result += "  <schema:title>{1}</schema:title>\n".format(self.prefix,
                        self)
        for key in self.items:
            result += "  <{0}:{1}>{2}</{0}:{1}>\n".format(self.prefix,
                    key, self.items[key])
        result += '</{0}:{1}>\n'.format(self.prefix, self.object_name)
        return result

