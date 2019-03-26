# -*- coding: utf-8 -*-
import sys

class Keyword:
    prefix = ""
    object_name = ""
    url = ""
    title = ""
    # various items, part of a keyword
    items = {}

    def __init__(self, prefix, object_name="keyword", url="", title=""):
        self.prefix = prefix
        self.object_name = object_name
        self.url = url
        self.title = title
        self.items = {}

    def __str__(self):
        return self.title

    def add_item(self, item, value):
        if item in self.items:
            self.items[item] += " " + value
        else:
            self.items[item] = value

    def rdfxml(self):
        result = ""
        result += '<{0}:{1} rdf:about="{2}">\n'.format(self.prefix,
                self.object_name, self.url)
        if self.title:
            result += "  <{0}:displayName>{1}</{0}:displayName>\n".format(self.prefix, self.title)
        result += "  <schema:title>{0}</schema:title>\n".format(self.title)
        for key in self.items:
            result += "  <{0}:{1}>{2}</{0}:{1}>\n".format(self.prefix,
                    key, self.items[key])
        result += '</{0}:{1}>\n'.format(self.prefix, self.object_name)
        return result

