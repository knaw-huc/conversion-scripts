# -*- coding: utf-8 -*-
import argparse
from datetime import datetime
import glob
import html
from html.parser import HTMLParser
from html.entities import name2codepoint
from html.entities import html5
import locale
locale.setlocale(locale.LC_ALL, 'nl-NL')
import os.path
import re
import sys
import unicodedata

class MyHTMLParser(HTMLParser):

    tags = []
    locals = locals()
    afk = ""
    in_datum = False
    in_jaar = False
    in_maand = False
    in_dag = False
    dag = ""
    maand = ""
    jaar = ""
    level = 1
    filename = ""
    pattern = re.compile("[^a-z]+")
    current_tag = ""
    current_data = ""
    tags_without_resource = ['addressee', 'archival_section_number', 'author', 'besluit_invnr', 'decisionmaker',
            'dossier', 'index_invnr', 'mailrapport_invnr', 'number_in_index', 'recipient', 'reference_kviv',
            'scan', 'secret', 'section_number', 'verbaal_found', 'verbaal_invnr']
    tags_with_resource = ['aantekeningen', 'link_scan', 'remarks', 'short_description', 'summary']
    entiteiten = []
    plaatsen = {}
    gemeenten = []
    provincies = []
    werkingsgebieden = []
    alt_namen = {}
    landelijke_bonden = {}
    regionale_bonden = {}
    data = ""
    in_alt_names = False
    in_speeldag = False
    in_landelijke_bond = False
    in_regionale_bond = False
    code = ""
    landelijke_bond = ""
    regionale_bond = ""
    beginjaar = ""
    eindjaar = ""
    opm_naam = ""
    in_literatuur = False
    auteur = ""
    title = ""
    plaats = ""
    jvu = ""
    pages = ""
    ppn = ""
    literatuur_over = {}
    publicaties_van = {}
    levensbeschouwingen = {}
    speeldagen = {}
    in_type_relatie = False
    relaties = {}
    relaties_met = []
    instelling = ""


    def __init__(self,output,collection,afk):
        super().__init__()
        self.output = output
        self.collection = collection
        self.afk = collection
        self.number = 1
        self.locals
#        for it in self.locals:
#            print(it)

    def add_attrs(self,attrs):
        res = ""
        for attr in attrs:
#            print(attr.__class__)
            res += ' {}="{}"'.format(attr[0],attr[1])
        return res   





    def vereniging_start(self,attrs):
        self.put_out("    <s:vereniging>")

    def vereniging_end(self):
        if not self.data.strip() == "":
            self.put_out(self.data.strip())
            self.data = ""
        self.put_out("</s:vereniging>\n")

    def tekst_start(self,attrs):
        self.put_out("    <s:tekst rdf:parseType=\"Literal\">")

    def tekst_end(self):
        if not self.data.strip() == "":
            self.put_out(self.data.strip())
            self.data = ""
        self.put_out("</s:tekst>\n")

    def plaats_start(self,attrs):
        pass
        #self.put_out("    <s:plaats>")

    def plaats_end(self):
        self.data = self.data.strip()
        if not self.data == "":
            code = self.make_id_from_words(self.data)
            if not self.data in self.plaatsen and not code=="":
                self.plaatsen[code] = self.data
            if not self.in_literatuur:
                self.put_out("    <s:plaats rdf:resource=\"https://resource.huygens.knaw.nl/sport/plaats/{0}\"/>\n".format(code))
            self.data = ""


    def gemeente_start(self,attrs):
        pass
#        self.put_out("    <s:gemeente>")

    def gemeente_end(self):
        self.data = self.data.strip()
        if not self.data == "":
            self.put_out("    <s:gemeente rdf:resource=\"https://resource.huygens.knaw.nl/sport/gemeente/{0}\"/>\n".format(self.data))
            if not self.data in self.gemeenten:
                self.gemeenten.append(self.data)
        self.data = ""

    def gemeente1984_start(self,attrs):
        pass
#        self.put_out("    <s:gemeente1984>")

    def gemeente1984_end(self):
        self.data = self.data.strip()
        if not self.data == "":
            self.put_out("    <s:gemeente1984 rdf:resource=\"https://resource.huygens.knaw.nl/sport/gemeente/{0}\"/>\n".format(self.data))
            if not self.data in self.gemeenten:
                self.gemeenten.append(self.data)
        self.data = ""

    def provincie_start(self,attrs):
        pass
#        self.put_out("    <s:provincie>")

    def provincie_end(self):
        self.data = self.data.strip()
        if not self.data.strip() == "":
            self.put_out("    <s:provincie rdf:resource=\"https://resource.huygens.knaw.nl/sport/provincie/{0}\"/>\n".format(self.data))
            if not self.data in self.provincies:
                self.provincies.append(self.data)
        self.data = ""

    def provincienaam_start(self,attrs):
        pass
#        self.put_out("    <s:provincienaam>")

    def provincienaam_end(self):
        pass
#        self.put_out("</s:provincienaam>")

    def naam_start(self,attrs):
        pass

    def naam_end(self):
        self.data = self.data.strip().replace(" & "," &amp; ")
        if not self.data == "":
            if self.in_alt_names:
                self.altname_code = "{0}_{1}".format(self.code, self.make_id_from_words(self.data))
                self.put_out("    <s:alternatieve_naam rdf:resource=\"https://resource.huygens.knaw.nl/sport/alt_namen/{0}\"/>\n".format(self.altname_code))
                if not self.altname_code in self.alt_namen:
                    self.alt_namen[self.altname_code] = {}
                    self.alt_namen[self.altname_code]['naam'] = self.data
            elif self.in_landelijke_bond:
                self.landelijke_bond = self.data
            elif self.in_regionale_bond:
                self.regionale_bond = self.data
            else:
                self.put_out("    <s:naam>{}</s:naam>\n".format(self.data))
        self.data = ""


    def opm_naam_start(self,attrs):
        pass
#        self.put_out("    <s:opm_naam>")

    def opm_naam_end(self):
        self.data = self.data.strip().replace(" & "," &amp; ")
        if not self.data == "":
            if self.in_alt_names:
                self.alt_namen[self.altname_code]['opm_naam'] = self.data
            elif self.in_landelijke_bond or self.in_regionale_bond:
                self.opm_naam = self.data
            else:
                self.put_out("    <s:opm_naam>{}</s:opm_naam>\n".format(self.data))
        self.data = ""

    
    def alternatieve_namen_start(self,attrs):
        self.in_alt_names = True

    def alternatieve_namen_end(self):
        self.in_alt_names = False


    def doelstelling_start(self,attrs):
        self.put_out("    <s:doelstelling rdf:parseType=\"Literal\">")

    def doelstelling_end(self):
        if not self.data.strip() == "":
            self.put_out(self.data.strip())
            self.data = ""
        self.put_out("</s:doelstelling>\n")

    def begindatum_start(self,attrs):
        pass
#        self.put_out("    <s:begindatum rdf:parseType=\"Resource\">")

    def begindatum_end(self):
        datum = self.get_datum()
        if not datum=="":
            self.put_out('    <s:begindatum rdf:datatype="http://www.w3.org/2001/XMLSchema#date">{1}</s:begindatum>\n'.format(self.afk, datum))
        self.jaar = ""
        self.maand = ""
        self.dag = ""

    def year_start(self,attrs):
        self.in_jaar = True

    def year_end(self):
        self.in_jaar = False

    def month_start(self,attrs):
        self.in_maand = True

    def month_end(self):
        self.in_maand = False

    def day_start(self,attrs):
        self.in_dag = True

    def day_end(self):
        self.in_dag = False

    def begindatum_soort_start(self,attrs):
        self.put_out("    <s:begindatum_soort>")

    def begindatum_soort_end(self):
        if not self.data.strip() == "":
            self.put_out(self.data.strip())
            self.data = ""
        self.put_out("</s:begindatum_soort>\n")

    def kb_start(self,attrs):
        pass
#        self.put_out("    <s:kb>")

    def kb_end(self):
        if not self.data.strip() == "":
            self.put_out("    <s:kb>{0}</s:kb>\n".format(self.data.strip()))
        self.data = ""

    def einddatum_start(self,attrs):
        pass
#        self.put_out("    <s:einddatum rdf:parseType=\"Resource\">")

    def einddatum_end(self):
        datum = self.get_datum()
        if not datum=="":
            self.put_out('    <s:einddatum rdf:datatype="http://www.w3.org/2001/XMLSchema#date">{0}</s:einddatum>\n'.format(datum))
        self.jaar = ""
        self.maand = ""
        self.dag = ""

    def einddatum_soort_start(self,attrs):
        pass
#        self.put_out("    <s:einddatum_soort>")

    def einddatum_soort_end(self):
        if not self.data.strip() == "":
            self.put_out("    <s:einddatum_soort>{0}</s:einddatum_soort>\n".format(self.data.strip()))
        self.data = ""

    def werkingsgebieden_start(self,attrs):
        pass
        #self.put_out("    <s:werkingsgebieden>")

    def werkingsgebieden_end(self):
        pass
        #self.put_out("  </s:werkingsgebieden>")

    def werkingsgebied_start(self,attrs):
        pass
#        self.put_out("    <s:werkingsgebied>")

    def werkingsgebied_end(self):
        if not self.data.strip() == "":
            self.data = self.data.strip()
            self.put_out("    <s:werkingsgebieden rdf:resource=\"https://resource.huygens.knaw.nl/sport/werkingsgebieden/{0}\"/>\n".format(self.data))
            if not self.data in self.werkingsgebieden:
                self.werkingsgebieden.append(self.data)
            self.data = ""
#        self.put_out("</s:werkingsgebied>")

    def sport_start(self,attrs):
        pass
#        self.put_out("    <s:sport>\n")

    def sport_end(self):
        pass
 #       if not self.data.strip() == "":
 #           self.put_out(self.data.strip())
 #           self.data = ""
 #       self.put_out("  </s:sport>\n")

    def soort_sport_start(self,attrs):
        self.put_out("    <s:soort_sport>")

    def soort_sport_end(self):
        if not self.data.strip() == "":
            self.put_out(self.data.strip())
            self.data = ""
        self.put_out("</s:soort_sport>\n")

    def landelijke_bond_start(self,attrs):
        self.in_landelijke_bond = True
        self.landelijke_bond = ""
        self.opm_naam = ""
        self.beginjaar = ""
        self.eindjaar = ""
        # self.put_out("    <s:Landelijke_bond rdf:parseType=\"Resource\">")

    def landelijke_bond_end(self):
        #           naam bewaren; make_id_from_words
        if self.in_landelijke_bond and not self.landelijke_bond=="":
            altname_code = "{0}_{1}".format(self.code, self.make_id_from_words(self.landelijke_bond))
            # meerdere malen zelfde landelijke bond is mogelijk!
            if altname_code in self.landelijke_bonden:
                altname_code = self.voeg_volgnr_toe(altname_code, self.landelijke_bonden)
#                stderr("code (l): {0}".format(altname_code))
            self.put_out("    <s:in_landelijke_bond rdf:resource=\"https://resource.huygens.knaw.nl/sport/inlandelijkebond/{0}\"/>\n".format(altname_code))
            if not altname_code in self.landelijke_bonden:
                bond = {}
                bond['naam'] = self.landelijke_bond
                bond['opm_naam'] = self.opm_naam
                bond['beginjaar'] = self.beginjaar
                bond['eindjaar'] = self.eindjaar
                self.landelijke_bonden[altname_code] = bond
                # beginjaar en eindjaar opslaan en hier pas toevoegen
                # anders komen ze bij de vorige
                # twee maal zelfde (landelijk bond komt ook voor; dan _2 aan code toevoegen (of _3?!)
        self.in_landelijke_bond = False


#        if not self.data.strip() == "":
#            self.put_out(self.data.strip())
#            self.data = ""
        # self.put_out("</s:Landelijke_bond>\n")

    def beginjaar_start(self,attrs):
        pass
#        self.put_out("    <s:beginjaar>")

    def beginjaar_end(self):
        self.data = self.data.strip()
        if not self.data == "":
            if self.in_landelijke_bond or self.in_regionale_bond:
                self.beginjaar = self.data
            else:
                self.put_out("    <s:beginjaar>{}</s:beginjaar>\n".format(self.data))
        self.data = ""


    def eindjaar_start(self,attrs):
        pass

    def eindjaar_end(self):
        self.data = self.data.strip()
        if not self.data == "":
            if self.in_landelijke_bond or self.in_regionale_bond:
                self.eindjaar = self.data
            else:
                self.put_out("    <s:eindjaar>{}</s:eindjaar>\n".format(self.data))
            self.data = ""


    def regionale_bond_start(self,attrs):
        self.in_regionale_bond = True
        self.regionale_bond = ""
        self.opm_naam = ""
        self.beginjaar = ""
        self.eindjaar = ""
#        self.put_out("    <s:regionale_bond rdf:parseType=\"Resource\">")

    def regionale_bond_end(self):
        if self.in_regionale_bond and not self.regionale_bond=="":
            altname_code = "{0}_{1}".format(self.code, self.make_id_from_words(self.regionale_bond))
            # meerdere malen zelfde regionale bond is mogelijk!
            if altname_code in self.regionale_bonden:
                altname_code = self.voeg_volgnr_toe(altname_code, self.regionale_bonden)
#                stderr("code (r): {0}".format(altname_code))
            self.put_out("    <s:in_regionale_bond rdf:resource=\"https://resource.huygens.knaw.nl/sport/inregionalebond/{0}\"/>\n".format(altname_code))
            if not altname_code in self.regionale_bonden:
                bond = {}
                bond['naam'] = self.landelijke_bond
                bond['opm_naam'] = self.opm_naam
                bond['beginjaar'] = self.beginjaar
                bond['eindjaar'] = self.eindjaar
                self.regionale_bonden[altname_code] = bond
        self.in_regionale_bond = False

    def speeldag_start(self,attrs):
        self.in_speeldag = True

    def speeldag_end(self):
        self.in_speeldag = False

    def dag_start(self,attrs):
        pass
#        self.put_out("    <s:dag>")

    def dag_end(self):
        self.data = self.data.strip()
        if not self.data == "":
            code = self.make_id_from_words(self.data)
            if not code in self.speeldagen:
               self.speeldagen[code] = self.data
               self.put_out("    <s:speeldag rdf:resource=\"https://resource.huygens.knaw.nl/sport/speeldag/{}\"/>\n".format(code))
            self.data = ""

    def levensbeschouwing_start(self,attrs):
        pass
#        self.put_out("    <s:levensbeschouwing>")

    def levensbeschouwing_end(self):
        self.data = self.data.strip()
        if not self.data == "":
            code = self.make_id_from_words(self.data)
            if not code in self.levensbeschouwingen:
                self.levensbeschouwingen[code] = self.data
            self.put_out("    <s:levensbeschouwing rdf:resource=\"https://resource.huygens.knaw.nl/sport/levensbeschouwing/{}\"/>\n".format(code))
            self.data = ""

    def nr_verenigingsdossier_start(self,attrs):
        pass
#        self.put_out("    <s:nr_verenigingsdossier>")

    def nr_verenigingsdossier_end(self):
        self.data = self.data.strip()
        if not self.data == "":
            self.put_out("    <s:nr_verenigingsdossier>{0}</s:nr_verenigingsdossier>\n".format(self.data))
            self.data = ""

    def relaties_start(self,attrs):
        pass
#        self.put_out("    <s:relaties>")

    def relaties_end(self):
        pass
#        self.data = self.data.strip()
#        if not self.data.strip() == "":
#            self.put_out(self.data.strip())
#            self.data = ""
#        self.put_out("  </s:relaties>\n")

    def relatie_start(self,attrs):
         pass
#        self.put_out("    <s:relatie rdf:parseType=\"Resource\">")

    def relatie_end(self):
        if not self.in_type_relatie:
#            self.put_out("  <s:relatie>\n")

            if not self.instelling=="":
                code = "{0}_{1}".format(self.code,
                    self.make_id_from_words(self.instelling))
                if not code in self.relaties:
                    relatie = {}
                    relatie['relaties_met'] = self.relaties_met
                    relatie['instelling'] = self.instelling
                    self.relaties[code] = relatie
                self.put_out("    <s:relatie rdf:resource=\"https://resource.huygens.knaw.nl/sport/relatie/{0}\"/>\n".format(code))
        else:
            self.data = self.data.strip()
            if not self.data == "":
                self.relaties_met.append(self.data)
                self.data = ""

#       if not self.data.strip() == "":
#            self.put_out(self.data.strip())
#            self.data = ""
#        self.put_out("  </s:relatie>\n")

    def type_relatie_start(self,attrs):
        self.in_type_relatie = True
        self.relaties_met = []
        self.instelling = ""
#        self.put_out("    <s:type_relatie>")

    def type_relatie_end(self):
        self.in_type_relatie = False
#       if not self.data.strip() == "":
#            self.put_out(self.data.strip())
#            self.data = ""
#        self.put_out("  </s:type_relatie>\n")

    def relatie_met_start(self,attrs):
        pass
#        self.put_out("    <s:relatie_met>")

    def relatie_met_end(self):
        self.data = self.data.strip()
        if not self.data == "":
            self.relaties_met.append(self.data)
            self.put_out(self.data.strip())
            self.data = ""
#        self.put_out("  </s:relatie_met>\n")

    def instelling_start(self,attrs):
        pass
#        self.put_out("    <s:instelling rdf:parseType=\"Literal\">")

    def instelling_end(self):
        self.data = self.data.strip()
        if not self.data == "":
            self.instelling = self.data
#            self.put_out("    <s:instelling rdf:parseType=\"Literal\">{0}</s:instelling>\n".format(self.data))
            self.data = ""

    def oprichters_start(self,attrs):
        pass
#        self.put_out("    <s:oprichters rdf:parseType=\"Literal\">")

    def oprichters_end(self):
        self.data = self.data.strip()
        if not self.data == "":
            self.put_out("    <s:oprichters rdf:parseType=\"Literal\">{}</s:oprichters>\n".format(self.data))
            self.data = ""

    def bestuursleden_start(self,attrs):
        pass
#        self.put_out("    <s:bestuursleden rdf:parseType=\"Literal\">")

    def bestuursleden_end(self):
        self.data = self.data.strip()
        if not self.data == "":
            self.put_out("    <s:bestuursleden rdf:parseType=\"Literal\">{}</s:bestuursleden>\n".format(self.data))
            self.data = ""

    def beschermheren_start(self,attrs):
        pass
#        self.put_out("    <s:beschermheren rdf:parseType=\"Literal\">")

    def beschermheren_end(self):
        self.data = self.data.strip()
        if not self.data == "":
            self.put_out("    <s:beschermheren rdf:parseType=\"Literal\">{}</s:beschermheren>\n".format(self.data))
            self.data = ""

    def verantwoording_gegevens_start(self,attrs):
        pass
#        self.put_out("    <s:verantwoording_gegevens rdf:parseType=\"Literal\">")

    def verantwoording_gegevens_end(self):
        self.data = self.data.strip()
        if not self.data == "":
            self.put_out("    <s:verantwoording_gegevens rdf:parseType=\"Literal\">{}</s:verantwoording_gegevens>\n".format(self.data))
            self.data = ""

    def archief_geschreven_start(self,attrs):
        pass
#        self.put_out("    <s:archief_geschreven rdf:parseType=\"Literal\">")

    def archief_geschreven_end(self):
        self.data = self.data.strip()
        if not self.data == "":
            self.put_out("    <s:archief_geschreven rdf:parseType=\"Literal\">{}</s:archief_geschreven>\n".format(self.data))
            self.data = ""

    def archief_objecten_start(self,attrs):
        pass
#        self.put_out("    <s:archief_objecten rdf:parseType=\"Literal\">")

    def archief_objecten_end(self):
        self.data = self.data.strip()
        if not self.data == "":
            self.put_out("    <s:archief_objecten rdf:parseType=\"Literal\">{}</s:archief_objecten>\n".format(self.data))
            self.data = ""

    def eigen_gebouw_start(self,attrs):
        pass
#        self.put_out("    <s:eigen_gebouw rdf:parseType=\"Literal\">")

    def eigen_gebouw_end(self):
        self.data = self.data.strip()
        if not self.data == "":
            self.put_out("    <s:eigen_gebouw rdf:parseType=\"Literal\">{}</s:eigen_gebouw>\n".format(self.data))
            self.data = ""

    def vergaderplaats_start(self,attrs):
        pass
#        self.put_out("    <s:vergaderplaats rdf:parseType=\"Literal\">")

    def vergaderplaats_end(self):
        self.data = self.data.strip()
        if not self.data == "":
            self.put_out("    <s:vergaderplaats rdf:parseType=\"Literal\">{}</s:vergaderplaats>\n".format(self.data))
            self.data = ""

    def literatuur_over_start(self,attrs):
        pass
#        self.put_out("    <s:literatuur_over>")

    def literatuur_over_end(self):
        pass
#       if not self.data.strip() == "":
#           self.put_out(self.data.strip())
#           self.data = ""
#       self.put_out("</s:literatuur_over>\n")

    def literatuur_start(self,attrs):
        self.in_literatuur = True
        self.auteur = ""
        self.title = ""
        self.plaats = ""
        self.jvu = ""
        self.pages = ""
        self.ppn = ""
        #self.put_out("    <s:literatuur rdf:parseType=\"Resource\">")

    def literatuur_end(self):
        self.in_literatuur = False
        if not self.title == "":
            code = "{0}_{1}".format(self.code, self.make_id_from_words(self.title))
            if code in self.literatuur_over:
                code = self.voeg_volgnr_toe(code, self.literatuur_over)
            literatuur = {}
            literatuur['auteur'] = self.auteur
            literatuur['title'] = self.title
            literatuur['plaats'] = self.plaats
            literatuur['jvu'] = self.jvu
            literatuur['pages'] = self.pages
            literatuur['ppn'] = self.ppn
            self.literatuur_over[code] = literatuur
            self.put_out("    <s:literatuur_over rdf:resource=\"https://resource.huygens.knaw.nl/sport/literatuur_over/{}\"/>\n".format(code))
        self.data = ""
        #self.put_out("</s:literatuur>\n")

    def auteur_start(self,attrs):
        pass
#        self.put_out("    <s:auteur>")

    def auteur_end(self):
        self.data = self.data.strip()
        if not self.data == "":
            self.auteur = self.data
            #self.auteur = self.data
#            self.put_out("    <s:auteur>{}</s:auteur>\n".format(self.data))
            self.data = ""

    def title_start(self,attrs):
        pass
#       self.put_out("    <s:title>")

    def title_end(self):
        self.data = self.data.strip()
        if not self.data == "":
            self.title= self.data
#           self.put_out(self.data)
            self.data = ""
#        self.put_out("</s:title>\n")

    def jvu_start(self,attrs):
        pass
#       self.put_out("    <s:jvu>")

    def jvu_end(self):
        self.data = self.data.strip()
        if not self.data == "":
            self.jvu = self.data
#           self.put_out(self.data)
            self.data = ""
#        self.put_out("</s:jvu>\n")

    def pages_start(self,attrs):
        pass
#       self.put_out("    <s:pages>")

    def pages_end(self):
        self.data = self.data.strip()
        if not self.data == "":
            self.pages = self.data
#           self.put_out(self.data)
            self.data = ""
#        self.put_out("</s:pages>\n")

    def ppn_start(self,attrs):
        pass
#       self.put_out("    <s:ppn>")

    def ppn_end(self):
        self.data = self.data.strip()
        if not self.data == "":
            self.ppn = self.data
#           self.put_out(self.data)
            self.data = ""
#        self.put_out("</s:ppn>\n")

    def publicaties_van_start(self,attrs):
        pass
#        self.put_out("    <s:publicaties_van>")

    def publicaties_van_end(self):
        pass
#        if not self.data.strip() == "":
#            self.put_out(self.data.strip())
#            self.data = ""
#        self.put_out("</s:publicaties_van>\n")

    def publicaties_start(self,attrs):
        self.in_literatuur = True
        self.auteur = ""
        self.title = ""
        self.plaats = ""
        self.jvu = ""
        self.pages = ""
        self.ppn = ""
#        self.put_out("    <s:publicaties rdf:parseType=\"Resource\">")

    def publicaties_end(self):
        self.in_literatuur = False
        if not self.title == "":
            code = "{0}_{1}".format(self.code, self.make_id_from_words(self.title))
            if code in self.publicaties_van:
                code = self.voeg_volgnr_toe(code, self.publicaties_van)
            literatuur = {}
            literatuur['auteur'] = self.auteur
            literatuur['title'] = self.title
            literatuur['plaats'] = self.plaats
            literatuur['jvu'] = self.jvu
            literatuur['pages'] = self.pages
            literatuur['ppn'] = self.ppn
            self.literatuur_over[code] = literatuur
            self.put_out("    <s:publicatie_van rdf:resource=\"https://resource.huygens.knaw.nl/sport/publicatie_van/{}\"/>\n".format(code))
        self.data = ""

    def goossens_start(self,attrs):
        pass
#        self.put_out("    <s:goossens>")

    def goossens_end(self):
        self.data = self.data.strip()
        if not self.data == "":
            self.put_out("    <s:goossens>{0}</s:goossens>\n".format(self.data))
            self.data = ""

    def opmerkingen_start(self,attrs):
        pass
#        self.put_out("    <s:opmerkingen rdf:parseType=\"Literal\">")

    def opmerkingen_end(self):
        self.data = self.data.strip()
        if not self.data == "":
            self.put_out("    <s:opmerkingen rdf:parseType=\"Literal\">{0}</s:opmerkingen>\n".format(self.data))
            self.data = ""

    def aantekeningen_start(self,attrs):
        self.put_out("    <s:aantekeningen rdf:parseType=\"Literal\">")

    def aantekeningen_end(self):
        self.data = self.data.strip()
        if not self.data.strip() == "":
            self.put_out(self.data.strip())
            self.data = ""
        self.put_out("</s:aantekeningen>\n")

    def titel_start(self,attrs):
        self.put_out("    <s:titel>")

    def titel_end(self):
        self.data = self.data.strip()
        if not self.data.strip() == "":
            self.put_out(self.data.strip())
            self.data = ""
        self.put_out("</s:titel>\n")

    def annotatie_start(self,attrs):
        self.put_out("    <s:annotatie>")

    def annotatie_end(self):
        if not self.data.strip() == "":
            self.put_out(self.data.strip())
            self.data = ""
        self.put_out("  </s:annotatie>\n")

    def anno_start(self,attrs):
        self.put_out("\n  <s:anno rdf:parseType=\"Resource\">")

    def anno_end(self):
        self.data = self.data.strip()
        if not self.data.strip() == "":
            self.put_out(self.data.strip())
            self.data = ""
        self.put_out("</s:anno>")

    def ankernaam_start(self,attrs):
        self.put_out("    <s:ankernaam>")

    def ankernaam_end(self):
        self.data = self.data.strip()
        if not self.data.strip() == "":
            self.put_out(self.data.strip())
            self.data = ""
        self.put_out("</s:ankernaam>\n")

    def annotatie_tekst_start(self,attrs):
        self.put_out("    <s:annotatie_tekst rdf:parseType=\"Literal\">")

    def annotatie_tekst_end(self):
        self.data = self.data.strip()
        if not self.data.strip() == "":
            self.put_out(self.data.strip())
            self.data = ""
        self.put_out("</s:annotatie_tekst>\n")


    def tag_string(self, tag, literal=False):
        text = self.clean_text(self.current_data)
        self.current_data = ""
        if text=="":
            return
        lit_str = ''
        if literal:
            lit_str = ' rdf:parseType="Literal"'
        self.put_out("    <{0}:{1}{3}>{2}</{0}:{1}>\n".format(self.afk, tag, text, lit_str))


    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        r = self.locals
        if self.level == 1:
            self.code = (os.path.basename(self.filename)[:-4]).lower()
            self.number += 1
            lines = '''
  <{0}:{1} rdf:about="https://resource.huygens.knaw.nl/{0}/{1}/{2}">
'''
            self.put_out(lines.format(collection, tag, self.code))
        elif tag in self.tags_without_resource:
            pass
        elif tag in self.tags_with_resource:
            pass
        else:
            try:
                res = r[tag+"_start"]
                res(self,self.handle_attrs(attrs))
            except KeyError:
                if tag not in self.tags:
                    self.tags.append(tag)
        self.inc_level()
 
#print("Oops!  No start function for {}. Try\
                    #again...".format(tag))
            #print("<{}{}>".format(tag,self.add_attrs(attrs)))
          #  print("Start tag:", tag+"_start")
          #  for attr in attrs:
        #      print("     attr:", attr)


    def handle_endtag(self, tag):
        code = os.path.basename(self.filename)[:-4]
        if self.level == 2:
            self.put_out("  </{0}:{1}>\n".format(collection, tag))
            self.in_verbaal = False
            self.in_besluit = False
            self.in_mailrapport = True
        elif tag in self.tags_without_resource:
            self.tag_string(tag)
        elif tag in self.tags_with_resource:
            self.tag_string(tag, True)
        else:
            try:
                self.locals[tag+"_end"](self)
            except KeyError:
                pass
        if not self.data.strip() == "":
            self.put_out(self.data.strip())
            self.data = ""
        self.dec_level() # -= 1

    def handle_data(self, data):
        if self.in_jaar:
            self.jaar = data.strip()
            data = ""
        elif self.in_maand:
            self.maand = data.strip()
            data = ""
        elif self.in_dag:
            self.dag = data.strip()
            data = ""
        if not data == "":
            self.data = self.data + " " + data
#   

    def handle_comment(self, data):
        pass
        #print("Comment  :", data)

    def handle_entityref(self, name):
        pass
        #c = chr(name2codepoint[name])
        #print("Named ent:", c)

    def handle_charref(self, name):
        pass
        #if name.startswith('x'):
            #c = chr(int(name[1:], 16))
        #else:
            #c = chr(int(name))
        #print("Num ent  :", c)

    def handle_decl(self, data):
        pass
        #print("Decl     :", data)

    def handle_attrs(self, attrs):
        res = {}
        for a in attrs:
            res[a[0]] = a[1]
        return res
#        sys.stderr.write("len(attrs): {}\n{}\n".format(len(attrs),attrs))
#        for i in range(0,len(attrs),2):
#            res[attrs[i]] = attrs[i+1]
#            sys.stderr.write("i: {}\n".format(i))
#        return res



    def make_id_from_words(self,text):
        if self.pattern.search(text):
            text_id = self.pattern.sub("_",text.lower()).strip('_')
            # strip('_') pas uitvoeren als probleem upper lower etc is
            # opgelost
            return text_id
        else:
            return text

    def clean_text(self,text):
        entiteiten = re.finditer(r"(&[^ ;]+)(.)", text)
        for ent in entiteiten:
            ent_s = "{}{}".format(ent.group(1),ent.group(2))
            if ent_s not in self.entiteiten:
                self.entiteiten.append(ent_s)
#        text = re.sub(r"</p> *<p>","\n",text.strip())
        text = re.sub(r"</p> *<p>","</p>\n<p>",text.strip())
#        if text[0:3]=="<p>":
#            text = text[3:]
#        if text[-4:]=="</p>":
#            text = text[0:-4]
#        text = text.strip()
#        if text[-3:]=="<p>":
#            text = text[0:-3].strip()

        # Ja, ja... Dit moet echt drie keer gebeuren voordat alles is
        # omgezet naar utf8!
        text = html.unescape(html.unescape(html.unescape(text)))
#        text = text.replace("<","&lt;")
#        text = text.replace(">","&gt;")
        text = text.replace("&","&amp;")
        return text.strip()

    def inc_level(self):
        self.level += 1

    def dec_level(self):
        if self.level > 1:
            self.level -= 1
        
    def make_indent(self, num=0):
        if num==0:
            res = "  " * self.level
        else:
            res = "  " * num
        return res

    def put_out(self, arg):
        self.output.write(arg)


    def get_datum(self):
        dag = ""
        maand = ""

        if not len(self.maand) == 0:
            try:
                maand = "-{:0>2d}".format(int(self.maand)) #sprintf("-%02d",@dag.to_i)
            except ValueError:
                stderr("maand: {}".format(self.maand))
#            maand = "-{:0>2d}".format(int(maand)) #sprintf("-%02d",@maand.to_i)
        if not len(self.dag) == 0:
            try:
                dag = "-{:0>2d}".format(int(self.dag)) #sprintf("-%02d",@dag.to_i)
            except ValueError:
                stderr(dag)
        return '{}{}{}'.format(self.jaar,maand,dag)

    def verwerk_datum(self):
        result = '<{1}:date rdf:datatype="http://www.w3.org/2001/XMLSchema#date">{2}</{1}:date>'
        return result.format(self.make_indent(),self.afk,self.get_datum())

    def voeg_volgnr_toe(self, code, verzameling):
        while code in verzameling:
            md = re.match(r"(.*)_(\d+)$", code)
            if not md==None:
#                 stderr("iets gevonden")
#                 stderr("{0}".format(md.group(1)))
#                 stderr("{0}".format(md.group(2)))
                 code = "{0}_{1}".format(md.group(1), (int(md.group(2)) + 1))
            else:
                code = code + "_1"
#            stderr("code (v): {0}".format(code))
        return code

def help_message():
    stderr("use: python gd_politiek_parser.py -d directory -c collection -o output")
    sys.exit(0)


def stderr(text):
    sys.stderr.write("{}\n".format(text))


def arguments():
    ap = argparse.ArgumentParser(description='Read and convert files from "godsdienstpolitiek"')
    ap.add_argument('-y', '--jaar',
                    help="jaar"
                    )
    ap.add_argument('-i', '--inputfile',
                    help="inputfile" )
    ap.add_argument('-d', '--directory',
                    help="directory" )
    ap.add_argument('-c', '--collection',
                    help="collection" )
    ap.add_argument('-o', '--outputfile',
                    help="outputfile" )
    ap.add_argument('-r', '--resource',
                    help="resource",
                    default = "https://resource.huygens.knaw.nl/ingforms/gpol" )
    args = vars(ap.parse_args())
    return args


if __name__ == "__main__":
    stderr("start")
    stderr(datetime.today().strftime("%H:%M:%S"))


    args = arguments()
#    inputfile = args['inputfile']
    directory = args['directory']
    outputfile = args['outputfile']
    collection = args['collection']
#    resource = args['resource']
    if not directory or not outputfile or not collection:
        help_message()

    afk = collection[0:1]
    output = open(outputfile,"w", encoding='utf-8')
    # evt. aanpassen:
    rdf_rdf ='''<?xml version="1.0"?>
<rdf:RDF
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:{collection}="https://resource.huygens.knaw.nl/{collection}"
    xmlns:s="https://resource.huygens.knaw.nl/{collection}"
    xmlns:schema="http://schema.org/">
'''
    output.write(rdf_rdf.format(afk=afk,collection=collection))

    all_files = glob.glob("{}/**/*.xml".format(directory),recursive=True)
    # verwijder alles met adviesKIZ uit all_files


    parser = MyHTMLParser(output,collection,afk)

    for filename in all_files:
        if not "adviesKIZ" in filename:
#            stderr(filename)
            invoer = open(filename, encoding='utf-8')
            parser.filename = filename
            for line in invoer:
                parser.feed(line)

    output.write("\n")
    for key in sorted(parser.alt_namen):
        alt_name = parser.alt_namen[key]
        try:
            opm_name = '\n    <sport:opm_name>{0}</sport:opm_name>'.format(alt_name['opm_naam'])
        except KeyError:
            opm_name = ""
        
        keyword_lines = \
'''  <sport:alt_namen rdf:about="https://resource.huygens.knaw.nl/sport/alt_mamen/{0}">
    <sport:id>{0}</sport:id>
    <sport:alt_name>{1}</sport:alt_name>{2}
    <schema:title>{1}</schema:title>
  </sport:alt_namen>
'''.format(key, alt_name['naam'], opm_name)
        output.write(keyword_lines)

    output.write("\n")
    for key in sorted(parser.landelijke_bonden):
        bond = parser.landelijke_bonden[key]
        try:
            if not bond['opm_naam'] == "":
                opm_name = '\n    <sport:opm_name>{0}</sport:opm_name>'.format(bond['opm_naam'])
            else:
                opm_name = ""
        except KeyError:
            opm_name = ""
        try:
            if not bond['beginjaar'] == "":
                beginjaar = '\n    <sport:beginjaar>{0}</sport:beginjaar>'.format(bond['beginjaar'])
            else:
                beginjaar = ""
        except KeyError:
            beginjaar = ""
        try:
            if not bond['eindjaar'] == "":
                eindjaar = '\n    <sport:eindjaar>{0}</sport:eindjaar>'.format(bond['eindjaar'])
            else:
                eindjaar = ""
        except KeyError:
            eindjaar = ""
        
        keyword_lines = \
'''  <sport:inlandelijkebond rdf:about="https://resource.huygens.knaw.nl/sport/inlandelijkebond/{0}">
    <sport:id>{0}</sport:id>
    <schema:title>{1}</schema:title>{2}{3}{4}
  </sport:inlandelijkebond>
'''.format(key, bond['naam'], opm_name, beginjaar, eindjaar)
        output.write(keyword_lines)


    output.write("\n")
    for key in sorted(parser.regionale_bonden):
        bond = parser.regionale_bonden[key]
        try:
            if not bond['opm_naam'] == "":
                opm_name = '\n    <sport:opm_name>{0}</sport:opm_name>'.format(bond['opm_naam'])
            else:
                opm_name = ""
        except KeyError:
            opm_name = ""
        try:
            if not bond['beginjaar'] == "":
                beginjaar = '\n    <sport:beginjaar>{0}</sport:beginjaar>'.format(bond['beginjaar'])
            else:
                beginjaar = ""
        except KeyError:
            beginjaar = ""
        try:
            if not bond['eindjaar'] == "":
                eindjaar = '\n    <sport:eindjaar>{0}</sport:eindjaar>'.format(bond['eindjaar'])
            else:
                eindjaar = ""
        except KeyError:
            eindjaar = ""
        
        keyword_lines = \
'''  <sport:inregionalebond rdf:about="https://resource.huygens.knaw.nl/sport/inregionalebond/{0}">
    <sport:id>{0}</sport:id>
    <schema:title>{1}</schema:title>{2}{3}{4}
  </sport:inregionalebond>
'''.format(key, bond['naam'], opm_name, beginjaar, eindjaar)
        output.write(keyword_lines)


    output.write("\n")
    for code in sorted(parser.literatuur_over):
        literatuur = parser.literatuur_over[code]
        items = ""
        for key in literatuur:
            if not literatuur[key] == "":
                items = '{0}    <sport:{1}>{2}</sport:{1}>\n'.format(items, key, literatuur[key])
        
        lines = \
'''  <sport:literatuur_over rdf:about="https://resource.huygens.knaw.nl/sport/literatuur_over/{0}">
    <sport:id>{0}</sport:id>
    {1}    <schema:title>{2}</schema:title>
  </sport:literatuur_over>
'''.format(code, items, literatuur['title'])
        output.write(lines)


    output.write("\n")
    for code in sorted(parser.publicaties_van):
        literatuur = parser.publicaties_van[code]
        items = ""
        for key in literatuur:
            if not literatuur[key] == "":
                items = '{0}    <sport:{1}>{2}</sport:{1}>\n'.format(items, key, literatuur[key])
        
        lines = \
'''  <sport:publicatie_van rdf:about="https://resource.huygens.knaw.nl/sport/publicatie_van/{0}">
    <sport:id>{0}</sport:id>
    {1}    <schema:title>{2}</schema:title>
  </sport:publicatie_van>
'''.format(code, items, literatuur['title'])
        output.write(lines)


    output.write("\n")
    for code in sorted(parser.levensbeschouwingen):
        levensbeschouwing = parser.levensbeschouwingen[code]
        lines = \
'''  <sport:levensbeschouwing rdf:about="https://resource.huygens.knaw.nl/sport/levensbeschouwing/{0}">
    <sport:id>{0}</sport:id>
    <schema:title>{1}</schema:title>
  </sport:levensbeschouwing>
'''.format(code, levensbeschouwing)
        output.write(lines)

    output.write("\n")
    for code in sorted(parser.speeldagen):
        speeldag = parser.speeldagen[code]
        lines = \
'''  <sport:speeldag rdf:about="https://resource.huygens.knaw.nl/sport/speeldag/{0}">
    <sport:id>{0}</sport:id>
    <schema:title>{1}</schema:title>
  </sport:speeldag>
'''.format(code, speeldag)
        output.write(lines)

    output.write("\n")
    for code in sorted(parser.plaatsen):
        plaats = parser.plaatsen[code]
        lines = \
'''  <sport:plaats rdf:about="https://resource.huygens.knaw.nl/sport/plaats/{0}">
    <sport:id>{0}</sport:id>
    <schema:title>{1}</schema:title>
  </sport:plaats>
'''.format(code, plaats)
        output.write(lines)

    output.write("\n")
    for code in sorted(parser.gemeenten):
#        gemeente = parser.gemeenten[code]
        lines = \
'''  <sport:gemeente rdf:about="https://resource.huygens.knaw.nl/sport/gemeente/{0}">
    <sport:id>{0}</sport:id>
    <schema:title>{0}</schema:title>
  </sport:gemeente>
'''.format(code)
        output.write(lines)

    output.write("\n")
    for code in sorted(parser.provincies):
        lines = \
'''  <sport:provincie rdf:about="https://resource.huygens.knaw.nl/sport/provincie/{0}">
    <sport:id>{0}</sport:id>
    <schema:title>{0}</schema:title>
  </sport:provincie>
'''.format(code)
        output.write(lines)

    output.write("\n")
    for code in sorted(parser.relaties):
        relatie = parser.relaties[code]
#        stderr("relatie: {}".format(relatie))
        relatie_met = '/'.join(relatie['relaties_met'])
        instelling = relatie['instelling']
        lines = \
'''  <sport:relatie rdf:about="https://resource.huygens.knaw.nl/sport/provincie/{0}">
    <sport:id>{0}</sport:id>
    <schema:title>{1}</schema:title>
    <schema:relatie_met>{2}</schema:relatie_met>
    <schema:instelling>{1}</schema:instelling>
  </sport:relatie>
'''.format(code, instelling, relatie_met)
        output.write(lines)

    output.write("\n</rdf:RDF>\n")

    stderr("unknown tags ({}):".format(len(parser.tags)))
    for t in parser.tags:
        stderr("{}".format(t))

#    stderr("html entiteiten ({}):".format(len(parser.entiteiten)))
#    for t in parser.entiteiten:
#        stderr("{} - {}".format(t,html.unescape(t)))

    stderr(datetime.today().strftime("%H:%M:%S"))
    stderr("einde")

