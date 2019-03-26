# -*- coding: utf-8 -*-
from person import Person
from collective import Collective
import sys

class Document:
    prefix = ""
    object_name = ""
    url = ""
    title = ""
    # authors: a document might have multiple authors
    authors = []
    # publishers: a document might have multiple publishers
    publishers = []
    # various items, part of a publication
    items = {}

    def __init__(self, prefix, object_name="document", url="", title=""):
        self.prefix = prefix
        self.object_name = object_name
        self.url = url
        self.title = title

    def __str__(self):
        return self.title

    def add_author(self, author):
        if type(author) is Person:
            self.authors.append(author)
        else:
            sys.stderr.write("Can't add object {} as author; should be \
Person\n".format(author.__class__))

    def add_publisher(self, publisher):
        if type(publisher) is Collective:
            self.publishers.append(publisher)
        else:
            sys.stderr.write("Can't add object {} as publisher; should be \
Collective\n".format(publisher.__class__))

    def add_item(self, item, value):
        if item=="author":
            self.add_author(value)
        elif item=="publisher":
            self.add_publisher(value)
        elif item in self.items:
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
        for author in self.authors:
            result += '  <{0}:author rdf:resource="{1}"/>\n'.format(self.prefix, 
                    author.url)
        for publisher in self.publishers:
            result += '  <{0}:publisher rdf:resource="{1}"/>\n'.format(self.prefix, 
                    publisher.url)
        for item in self.items:
            print(item)
        result += '</{0}:{1}>\n'.format(self.prefix, self.object_name)
        for author in self.authors:
            result += author.rdfxml()
        for publisher in self.publishers:
            result += publisher.rdfxml()
        return result

