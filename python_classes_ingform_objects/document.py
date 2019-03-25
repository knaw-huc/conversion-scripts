# -*- coding: utf-8 -*-
from person import Person
import sys

class Document:
    prefix = ""
    url = ""
    title = ""
    # authors: a document might have multiple authors
    authors = []

    def __init__(self, prefix, url="", title=""):
        self.prefix = prefix
        if url:
            self.url = url
        if title:
            self.title = title

    def __str__(self):
        return self.title

    def add_author(self, author):
        if type(author) is Person:
            self.authors.append(author)
        else:
            sys.stderr.write("Can't add object {} as author; should be \
Person\n".format(author.__class__))

    def rdfxml(self):
        result = ""
        result += '<{0}:document rdf:about="{1}">\n'.format(self.prefix,
                self.url)
        if self.title:
            result += "  <{0}:displayName>{1}</{0}:displayName>\n".format(self.prefix, self.title)
        result += "  <schema:title>{0}</schema:title>\n".format(self.title)
        for author in self.authors:
            result += '  <{0}:author rdf:resource="{1}"/>\n'.format(self.prefix, 
                    author.url)
        result += '</{0}:document>\n'.format(self.prefix)
        for author in self.authors:
            result += author.rdfxml()
        return result

