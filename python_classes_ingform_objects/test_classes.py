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


if __name__ == '__main__':
    unittest.main()

