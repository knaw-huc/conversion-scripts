# -*- coding: utf-8 -*-
from person import Person
from collective import Collective
from language import Language
from location import Location
from document import Document
from keywords import Keyword
import unittest

class TestStringMethods(unittest.TestCase):

    def test_person(self):
        person = Person(prefix="ww", object_name="wwperson", url="https://resource.huygens.knaw.nl/ww/wwperson/43375aa3-1ed3-4a65-89ec-520794705415")
        person.add("baseSurname","Vries")
        person.add("surnamePrefix","de")
        person.add("givenName","Jan")
        person.add_item("remark","Is dit een echte naam of een pseudoniem?")
        self.assertEqual(str(person), "Jan de Vries")
        self.assertEqual(person.rdfxml().split('\n')[6],'  <schema:title>Jan de Vries</schema:title>')
        self.assertNotEqual(person.items,{})
        #
        person = Person(prefix="ww", object_name="wwperson",
                url="https://resource.huygens.knaw.nl/ww/wwperson/43375aa3-1ed3-4a65-89ec-520794705416")
        person.add("baseSurname","Vries")
        person.add("surnamePrefix","de")
        person.add("givenName","Teun")
        self.assertEqual(person.items,{})

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()


    person = Person(prefix="ww", url="http::/enz")

    person.add("baseSurname","Jansen")
    print("{}".format(person))

    person = Person(prefix="ww", object_name="wwperson", url="https://resource.huygens.knaw.nl/ww/wwperson/43375aa3-1ed3-4a65-89ec-520794705415")
    person.add("baseSurname","Vries")
    person.add("surnamePrefix","de")
    person.add("givenName","Jan")
    person.add_item("remark","Is dit een echte naam of een pseudoniem?")
    print("{}".format(person))
    print("{}".format(person.rdfxml()))

    taal = Language(language="Dutch", prefix="ww", object_name="wwlanguage")
    taal.add_item("remark","Ook wel bekend als 'Nederlands'")
    print(taal)
    print(taal.rdfxml())

    plaats = Location(location="Delft", prefix="ww",
            object_name="wwlocation")
    plaats.set_latitude("52° 1′ NB")
    plaats.set_longitude("4° 21′ OL")
    plaats.add_item("remakr","Locatie is ongeveer")
    print(plaats)
    print(plaats.rdfxml())

    doc = Document(prefix="ww",title="Een titel", object_name="wwdocument",
            url="https://blabla/etc/123456789")
    print(doc)
    print(doc.rdfxml())

    doc.add_author(person)
    doc.add_author("Jan Jansen")
    print(doc.rdfxml())

    coll = Collective(prefix="ww", collective="DI-HUC",
            object_name="wwinstitute")
    coll.add_item("remark","een dolle boel!")
    coll.add_location(Location(prefix="ww",location="Amsterdam", url="https://etc.etc/amsterdam"))
    print(coll)
    print(coll.rdfxml())
    print(plaats.rdfxml())

    uitgever = Collective(prefix="ww", collective="De Uitgeverij",
            url="https://resource.huygens.knaw.nl/ww/wwcollective/cc1fcc6c-fda0-4e26-af4e-554b845bfa1b",
            object_name="wwpublisher")

    doc.add_publisher(uitgever)

    doc.add_item("isbn","9870123456789")
    doc.add_item("author","Karel Appel")

    print(doc)
    print(doc.rdfxml())

    keyword = Keyword(prefix="ww", title="Education, general")
    keyword.add_item("nl","Onderwijs, algemeen")
    print(keyword)
    print(keyword.rdfxml())

    doc_2 = Document(prefix="ww",title="Nog een titel", object_name="wwdocument")
    print(doc_2)
    print(doc_2.rdfxml())
    doc_2.add_keyword(keyword)
    print(doc_2)
    print(doc_2.rdfxml())

