# -*- coding: utf-8 -*-
import html
import sys
import re
import unicodedata
import argparse

def uitvoer(txt):
    uitvoer_file.write(txt)

def stderr(text):
    sys.stderr.write("{}\n".format(text))

def start_table(line):
    global uitvoer_file
#    pattern = re.compile(r"`([^`]*)`")
    md = pattern.search(line)
    table = md.group(1)
#    stderr(table)
    if uitvoer_file:
        uitvoer("\n</rdf:RDF>\n")
        uitvoer_file.close()
    uitvoer_file = open("{}.xml".format(table),"w",encoding="utf-8")
    uitvoer('''<?xml version="1.0"?>
<rdf:RDF
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:schema="http://schema.org/"
    xmlns:pnv="http://www.curl.org/pnv"
    xmlns:names="https://resource.huygens.knaw.nl/names/"
    xmlns:{0}="https://resource.huygens.knaw.nl/names/{0}">
'''.format(table))
    return table

def split_item(item):
    res = item.split("','")
    new_res = []
    for r in res:
        if r.find("'")>-1 and r.find(",")>-1:
            new_res = new_res + r.split(",")
        else:
            new_res = new_res + [r]
    result = []
    for r in new_res:
        result.append(r.strip('"').strip("'"))
#        print(r.strip('"').strip("'"))
    if result[0]=="":
        return []
    return result


def makeArgParser():
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--inputfile',
                    help="inputfile. Default ./NAMES CORPUS 1.0 MySQL 5.5.sql",
                    default="./NAMES CORPUS 1.0 MySQL 5.5.sql"
                    )
    return ap

if __name__ == "__main__":

    ap = makeArgParser()
    args = vars(ap.parse_args())
    filename = args['inputfile']
    base = "https://resource.huygens.knaw.nl/names/"

    res = locals()["stderr"]
    #method_to_call = getattr(local(), 'stderr')

    stderr("start")

    tellers = dict()
    pattern = re.compile(r"`([^`]*)`")

    invoer = open(filename, encoding="utf-8")
    uitvoer_file = None # open("result.xml","w",encoding="utf-8")
    teller = 0
    table = ""
    new_table = False
    table_columns = []
    for line in invoer:
        if new_table:
            if line.isspace():
#                stderr("end new_table")
                new_table = False
                stderr("table {}: columns:".format(table))
                for column in table_columns:
                    stderr(column)
            else:
                try:
                    column = pattern.search(line).group(1)
                    table_columns.append(column)
                except AttributeError:
                    pass
        elif line.startswith("CREATE TABLE"):
            table = start_table(line)
            new_table = True
            table_columns = []
        elif line.startswith("INSERT INTO"):
#            res = re.findall('\(([^)]*)\)',line)
            res = line.split("),(")
            res[0] = res[0][res[0].find("("):]
            for item in res:
                item = item.strip("()")
                values = split_item(item)
                if len(values)>0:
                    uitvoer("\n")
                    if table=="names_gn_standard_relations":
                        identifier = "{}-{}".format(values[2],values[3])
                    elif table=="names_sns_standard_relations":
                        identifier = "{}-{}".format(values[2].strip("'"),values[3].strip("'")[4:])
                    else:
                        identifier = values[0].strip("'") 
                    uitvoer('''    <rdf:Description rdf:about="https://resource.huygens.knaw.nl/names/{0}/{1}">
        <rdf:type rdf:resource="https://resource.huygens.knaw.nl/names/{0}" />
'''.format(table,identifier))
                    tel = 0
                    for (col,val) in zip(table_columns, values):
                        tel += 1
    #                    val = html.escape(val.strip("'"))
                        val = val.strip("'")
                        val = val.replace(" & "," &amp; ")
                        val = val.replace("<","&lt;")
                        if table=="names_gn":
                            if tel==2:
                                uitvoer("        <schema:name>{1}</schema:name>\n".format(col,val))
                                uitvoer("        <pnv:givenName>{1}</pnv:givenName>\n".format(col,val))
                            if tel==14:
                                if val=="NULL":
                                    uitvoer("        <names:{0} rdf:resource=\"{1}\"/>\n".format(col,val))
                                else:
                                    new_val = "{}names_gn_standard/{}".format(base,val)
                                    uitvoer("        <names:{0} rdf:resource=\"{1}\"/>\n".format(col,new_val))
                            else:
                                uitvoer("        <schema:{0}>{1}</schema:{0}>\n".format(col,val))
                        elif table=="names_gn_pairs":
                            if tel==3:
                                uitvoer("        <schema:name>{0} / {1}</schema:name>\n".format(values[1].strip("'"),val))
                            if tel==6 or tel==7:
                                new_val = "{}names_gn/{}".format(base,val)
                                uitvoer("        <names:{0} rdf:resource=\"{1}\"/>\n".format(col,new_val))
                            elif tel==11 or tel==12:
                                new_val = "{}names_gn_standard/{}".format(base,val)
                                uitvoer("        <names:{0} rdf:resource=\"{1}\"/>\n".format(col,new_val))
                            else:
                                uitvoer("        <schema:{0}>{1}</schema:{0}>\n".format(col,val))
                        elif table=="names_gn_standard":
                            if tel==2:
                                uitvoer("        <schema:name>{1}</schema:name>\n".format(col,val))
                                uitvoer("        <pnv:givenName>{1}</pnv:givenName>\n".format(col,val))
                            uitvoer("        <schema:{0}>{1}</schema:{0}>\n".format(col,val))
                        elif table=="names_gn_standard_relations":
                            if tel==2:
                                uitvoer("        <schema:name>{0} / {1}</schema:name>\n".format(values[0].strip("'"),val))
                            if tel==3 or tel==4:
                                new_val = "{}names_gn_standard/{}".format(base,val)
                                uitvoer("        <names:{0} rdf:resource=\"{1}\"/>\n".format(col,new_val))
                            else:
                                uitvoer("        <schema:{0}>{1}</schema:{0}>\n".format(col,val))
                        elif table=="names_snf":
                            if tel==2:
                                uitvoer("        <schema:name>{1}</schema:name>\n".format(col,val))
                                uitvoer("        <pnv:baseSurname>{1}</pnv:baseSurname>\n".format(col,val))
                            if tel==3:
                                new_val = "{}names_snf_prefix/{}".format(base,val)
                                uitvoer("        <names:{0} rdf:resource=\"{1}\"/>\n".format(col,new_val))
                            else:
                                uitvoer("        <schema:{0}>{1}</schema:{0}>\n".format(col,val))
                        elif table=="names_snf_prefix":
                            if tel==2:
                                uitvoer("        <schema:name>{1}</schema:name>\n".format(col,val))
                                uitvoer("        <pnv:surnamePrefix>{1}</pnv:surnamePrefix>\n".format(col,val))
                            uitvoer("        <schema:{0}>{1}</schema:{0}>\n".format(col,val))
                        elif table=="names_sns":
                            if tel==2:
                                uitvoer("        <schema:name>{1}</schema:name>\n".format(col,val))
                                uitvoer("        <pnv:baseSurname>{1}</pnv:baseSurname>\n".format(col,val))
                            if tel==6:
                                new_val = "{}names_sns_standard/{}".format(base,val)
                                uitvoer("        <names:{0} rdf:resource=\"{1}\"/>\n".format(col,new_val))
                            else:
                                uitvoer("        <schema:{0}>{1}</schema:{0}>\n".format(col,val))
                        elif table=="names_sns_pairs":
                            if tel==6:
                                uitvoer("        <schema:name>{0} / {1}</schema:name>\n".format(values[4].strip("'"),val))
                            if tel==3 or tel==4:
                                if val.strip()=="":
                                    uitvoer("        <names:{0} />\n".format(col))
                                else:
                                    new_val = "{}names_sns/{}".format(base,val)
                                    uitvoer("        <names:{0} rdf:resource=\"{1}\"/>\n".format(col,new_val))
                            elif tel==9 or tel==10:
                                if val.strip()=="":
                                    uitvoer("        <names:{0} />\n".format(col))
                                else:
                                    new_val = "{}names_sns_standard/{}".format(base,val)
                                    uitvoer("        <names:{0} rdf:resource=\"{1}\"/>\n".format(col,new_val))
                            else:
                                uitvoer("        <schema:{0}>{1}</schema:{0}>\n".format(col,val))
                        elif table=="names_sns_standard":
                            if tel==2:
                                uitvoer("        <schema:name>{1}</schema:name>\n".format(col,val))
                                uitvoer("        <pnv:baseSurname>{1}</pnv:baseSurname>\n".format(col,val))
                            uitvoer("        <schema:{0}>{1}</schema:{0}>\n".format(col,val))
                        elif table=="names_sns_standard_relations":
                            if tel==2:
                                uitvoer("        <schema:name>{0} / {1}</schema:name>\n".format(values[0].strip("'"),val))
                            if tel==3 or tel==4:
                                new_val = "{}names_sns_standard/{}".format(base,val)
                                uitvoer("        <names:{0} rdf:resource=\"{1}\"/>\n".format(col,new_val))
                            else:
                                uitvoer("        <schema:{0}>{1}</schema:{0}>\n".format(col,val))
                        else:
                            uitvoer("        <schema:{0}>{1}</schema:{0}>\n".format(col,val))
                    uitvoer("    </rdf:Description>\n")
                
            if table in tellers:
                tellers[table] += len(res)
            else:
                tellers[table] = len(res)
            teller += len(res)

    uitvoer("\n</rdf:RDF>\n")
    uitvoer_file.close()

    stderr("counted {} items".format(teller))

    teller = 0
    for key in tellers.keys():
        stderr("{} has {} items".format(key,tellers[key]))
        teller += tellers[key]
    stderr("counted {} items".format(teller))
    stderr("end")
 

