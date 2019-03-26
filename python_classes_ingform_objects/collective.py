# -*- coding: utf-8 -*-


class Collective:
    prefix = ""
    object_name = ""
    url = ""
    collective = ""

    def __init__(self, prefix, object_name="collective", url="", collective=""):
        self.prefix = prefix
        self.object_name = object_name
        self.url = url
        self.collective = collective

    def __str__(self):
        return self.collective

    def rdfxml(self):
        result = ""
        result += '<{0}:{1} rdf:about="{2}">\n'.format(self.prefix,
                self.object_name, self.url)
        if self.collective:
            result += "  <{0}:displayName>{1}</{0}:displayName>\n".format(self.prefix,
                        self.collective)
        result += "  <schema:title>{1}</schema:title>\n".format(self.prefix,
                        self.collective)
        result += '</{0}:{1}>\n'.format(self.prefix, self.object_name)
        return result

