# -*- coding: utf-8 -*-


class Language:
    prefix = ""
    url = ""
    language = ""

    def __init__(self, prefix, url="", language=""):
        self.prefix = prefix
        if url:
            self.url = url
        if language:
            self.language = language

    def __str__(self):
        if self.language:
            return self.language
        return None

    def rdfxml(self):
        result = ""
        result += '<{0}:language rdf:about="{1}">\n'.format(self.prefix,
                self.url)
        if self.language:
            result += "  <{0}:displayName>{1}</{0}:displayName>\n".format(self.prefix,
                        self.language)
            result += "  <schema:title>{1}</schema:title>\n".format(self.prefix,
                        self.language)
        result += '</{0}:language>\n'.format(self.prefix)
        return result

