# -*- coding: utf-8 -*-


class Collective:
    prefix = ""
    url = ""
    collective = ""

    def __init__(self, prefix, url="", collective=""):
        self.prefix = prefix
        if url:
            self.url = url
        if collective:
            self.collective = collective

    def __str__(self):
        return self.collective

    def rdfxml(self):
        result = ""
        result += '<{0}:collective rdf:about="{1}">\n'.format(self.prefix,
                self.url)
        if self.collective:
            result += "  <{0}:displayName>{1}</{0}:displayName>\n".format(self.prefix,
                        self.collective)
        result += "  <schema:title>{1}</schema:title>\n".format(self.prefix,
                        self.collective)
        result += '</{0}:collective>\n'.format(self.prefix)
        return result

