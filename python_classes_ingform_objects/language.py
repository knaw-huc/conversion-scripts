# -*- coding: utf-8 -*-


class Language:
    prefix = ""
    object_name = ""
    url = ""
    language = ""
    items = {}

    def __init__(self, prefix, object_name="language", url="", language=""):
        self.prefix = prefix
        self.object_name = object_name
        self.url = url
        self.language = language
        self.items = {}

    def __str__(self):
        return self.language

    def add_item(self, item, value):
        if item in self.items:
            self.items[item] += " " + value
        else:
            self.items[item] = value

    def rdfxml(self):
        result = ""
        result += '<{0}:{1} rdf:about="{2}">\n'.format(self.prefix, self.object_name,
                self.url)
        if self.language:
            result += "  <{0}:displayName>{1}</{0}:displayName>\n".format(self.prefix,
                        self.language)
            result += "  <schema:title>{1}</schema:title>\n".format(self.prefix,
                        self.language)
        for key in self.items:
            result += "  <{0}:{1}>{2}</{0}:{1}>\n".format(self.prefix,
                    key, self.items[key])
        result += '</{0}:{1}>\n'.format(self.prefix, self.object_name)
        return result

