# -*- coding: utf-8 -*-
import re
from pnvperson import PnvPerson


class Person(PnvPerson):
    prefix = ""
    url = ""

    def __init__(self, prefix, url=""):
        PnvPerson.__init__(self)
        self.prefix = prefix
        if url:
            self.url = url
    
    def rdfxml(self):
        name = PnvPerson.to_h(self)
        result = ""
        result += '<{0}:person rdf:about="{1}">\n'.format(self.prefix,
                self.url)
        result += "  <{0}:name>\n".format(self.prefix)
        for key in name.keys():
            value = name[key].strip()
            if value:
                result += "    <pnv:{0}>{1}</pnv:{0}>\n".format(key, value)
        result += "  </{0}:name>\n".format(self.prefix)
        result += "  <schema:title>{1}</schema:title>\n".format(self.prefix,
                        self)
        result += '</{0}:person>\n'.format(self.prefix)
        return result

