# -*- coding: utf-8 -*-


class Language:
    prefix = ""
    object_name = ""
    url = ""
    language = ""

    def __init__(self, prefix, object_name="language", url="", language=""):
        self.prefix = prefix
        self.object_name = object_name
        self.url = url
        self.language = language

    def __str__(self):
        if self.language:
            return self.language
        return None

    def rdfxml(self):
        result = ""
        result += '<{0}:{1} rdf:about="{2}">\n'.format(self.prefix, self.object_name,
                self.url)
        if self.language:
            result += "  <{0}:displayName>{1}</{0}:displayName>\n".format(self.prefix,
                        self.language)
            result += "  <schema:title>{1}</schema:title>\n".format(self.prefix,
                        self.language)
        result += '</{0}:{1}>\n'.format(self.prefix, self.object_name)
        return result

