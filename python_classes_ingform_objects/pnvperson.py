# -*- coding: utf-8 -*-
import re
import sys
import unicodedata

class PnvPerson:

    categories = [
        "prefix",
        "givenName",
        "patronym",
        "givenNameSuffix",
        "infixTitle",
        "surnamePrefix",
        "baseSurname",
        "trailingPatronym",
        "honorificSuffix",
        "disambiguatingDescription"
    ]

    combinations = [
        "surname",
        "literalName",
        "firstName",
        "infix",
        "suffix"
    ]

    def __init__(self):
        self.naam = {}
        for cat in self.categories:
            self.naam[cat] = ''

    def add(self,categorie,value):
        if value=="":
            sys.stderr.write("empty categorie: {}\n".format(categorie))
        elif categorie in self.naam:
            self.naam[categorie] += " {}".format(value)
        else:
            sys.stderr.write("unknown categorie: {}\n".format(categorie))
            self.naam[categorie] = value

    def get(self,categorie):
        if categorie in self.combinations:
            return self.combine(categorie) 
        if categorie in self.categories:
            return self.clean(self.naam[categorie])
        return "unknown name part: {}".format(categorie)

    def combine(self,categorie):
        if(categorie == "literalName"):
            result = ""
            for cat in self.categories:
                if cat in self.naam:
                    result = result + " {}".format(self.naam[cat])
            return self.clean(result)
        elif(categorie == "surname"):
            return self.clean("{} {}".format(self.naam['surnamePrefix'],self.naam['baseSurname']))
        elif(categorie == "firstName"):
            return self.clean("{} {} {}".format(self.naam['givenName'],self.naam['patronym'],self.naam['givenNameSuffix']))
        elif(categorie == "infix"):
            return self.clean("{} {}".format(self.naam['infixTitle'],self.naam['surnamePrefix']))
        elif(categorie == "suffix"):
            return self.clean("{} {} {}".format(self.naam['trailingPatronym'],self.naam['honorificSuffix'],self.naam['disambiguatingDescription']))

    def clean(self,text):
        pattern = re.compile("  +")
        pattern_2 = re.compile("' ")
        result = re.sub(pattern," ",text)
        result = re.sub(pattern_2,"'",result)
        return result.strip()

    def to_h(self):
        return self.naam

    def __str__(self):
        return self.get("literalName")

# end class
