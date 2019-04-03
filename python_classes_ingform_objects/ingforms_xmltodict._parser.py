# -*- coding: utf-8 -*-
import argparse
import glob
import html
import xmltodict
import pprint
import re
import sys
from miscellanious import Misc

def arguments():
    ap = argparse.ArgumentParser(description='Read and convert files as indicated in the parameters file')
    ap.add_argument('-p', '--parameters',
                    help="parameters file" )
    args = vars(ap.parse_args())
    return args

def verwerk_params(params_file):
    params = {}
    invoer = open(params_file, encoding='utf-8')
    for line in invoer:
        if line.strip():
            if '=' in line:
                key,value = line.strip().split('=')
                pos = line.find(':')
                params[key.strip()] = value.strip()
            else:
                parts = line.strip().split(',')
                params[parts[0]] = parts[1:]
    return params


def get_date(date, contents=[]):
    year = date.pop('year','')
    if not year:
        year = ''
    month = date.pop('month','')
    if not month:
        month = ''
    day = date.pop('day','')
    if not day:
        day = ''
    return "{}-{}-{}".format(year,month,day).strip('- ')

def remove_empty_tags(doc):
    remove = []
    keys = list(doc)
    for key in keys:
        if not doc[key]:
            remove.append(key)
    for key in remove:
        doc.pop(key)

def clean_text(text):
    text = re.sub(r"</p> *<p>","</p>\n<p>",text.strip())
    # Ja, ja... Dit moet echt drie keer gebeuren voordat alles is
    # omgezet naar utf8!
    text = html.unescape(html.unescape(html.unescape(text)))
    text = text.replace("&","&amp;")
#    sys.stderr.write("{}\n".format(text.strip()))
    return text.strip()

def add_link(new_link, url, prefix, k):
    return 


def process_link(db_object, k, doc, new_items, new_name):
    if not k in new_items:
        new_items[k] = {}
    res = []
    sys.stderr.write("doc_class: {0}\n".format(doc.__class__))
    for key in list(doc):
        sys.stderr.write("not list: {0}\n{1}\n".format(key,doc))
        word = doc[key]
        if isinstance(word,list):
            for w in word:
                ident = Misc.make_id_from_words(w)
                res.append([ident,w])
        else:
            ident = Misc.make_id_from_words(word)
            res.append([ident,word])
    sys.stderr.write("res: {0}\n".format(res))
    doc = []
    for item in res:
        sys.stderr.write("item: {0}\n".format(item))
        new_link = [item[1],"{0}/{1}/{2}/{3}".format(url, prefix, new_name, item[0])]
        doc.append({'@rdf:resource': new_link[1]})
    if not new_link[0] in new_items[k]:
        new_items[k][new_link[0]] = new_link[1]
    return doc


if __name__ == "__main__":

    Misc.start()
    global params
    global prefix
    global url
    global new_items
    
    args = arguments()
    parametersfile = args['parameters']
    params = verwerk_params(parametersfile)
    directory = params['directory']
    outputfile = params['outputfile']
    prefix = params['prefix']
    url = params['url']

    all_files = glob.glob("{}/**/*.xml".format(directory),recursive=True)

    result = {}
    result['rdf:RDF'] = {}
    result['rdf:RDF']['@xmlns:rdf'] = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    result['rdf:RDF']['@xmlns:schema'] = "http://schema.org/"
    result['rdf:RDF']['@xmlns:'+prefix] = url+"/"+prefix
    result['rdf:RDF']['rdf:Description'] = []

    new_items = {}

    for filename in all_files:
        invoer = open(filename, encoding='utf-8')
        pp = pprint.PrettyPrinter(indent=4)
        with open(filename, "rb") as fd:
            id = Misc.make_id_from_words(filename.split('\\')[-1][0:-4])
            doc = xmltodict.parse(invoer.read())
            if True:
                keys = list(doc)
                db_object = keys[0]
                remove_empty_tags(doc[db_object])
                keys = list(doc[db_object])
                for k in keys:
                    if k in params:
                        current_obj = doc[db_object][k]
                        doc[db_object][k] = []
                        type_obj = params[k][0]
                        if len(params[k])>1:
                            new_name = params[k][1]
                        else:
                            new_name = k
                        if len(params[k])>2:
                            contents = params[k][2]
                        if type_obj=='date':
                            new_date = get_date(current_obj, contents)
                            if new_date:
                                current_obj['#text'] = new_date
                                current_obj['@rdf:datatype'] = "http://www.w3.org/2001/XMLSchema#date"
                                doc[db_object][k] = current_obj
                            else:
                                doc[db_object].pop(k)
                        elif type_obj=='link':
                            res_links = process_link(db_object, k, current_obj, new_items,
                                    new_name)
                            sys.stderr.write("res_links: {}\n".format(res_links))
                            doc[db_object][prefix+":"+new_name] = res_links

                    if k in list(doc[db_object]):
                        sys.stderr.write("{}: {}\n".format(k, doc[db_object][k]))
                        if prefix+":"+k in doc[db_object]:
                            doc[db_object].pop(k)
                        else:
                            doc[db_object][prefix+":"+k] = doc[db_object].pop(k)


#                    if k in literals:
#                        doc[key][k] = { '#text':
#                                clean_text(doc[key].pop(k)) } #,
#                                '@rdf:parseType': "Literal"}
#                        sys.stderr.write("{}\n".format(doc[key][k]))

                  #  doc[key][prefix+":"+k] = doc[key].pop(k)
                sys.stderr.write("object: {}\n".format(doc[db_object]))
                for k in list(doc[db_object]):
                    sys.stderr.write("{}: {}\n".format(k, doc[db_object][k]))
                doc[db_object]['@rdf:about'] = "{3}/{1}/{2}/{0}".format(id,
                        prefix, db_object, url)
                result['rdf:RDF']['rdf:Description'].append(doc.pop(db_object))
                '''            except KeyError as err:
                keys = list(doc)
                sys.stderr.write("KeyError:\n{0}\n".format(keys))
                sys.stderr.write("err: {0}\n".format(err))
                sys.stderr.write("err: {0}\n".format(err.args)) '''


    for item in new_items:
#        sys.stderr.write("{}\n".format(item))
        if not item in doc:
            doc[item] = []
        for subitem in new_items[item]:
#            sys.stderr.write("{}\n".format(subitem))
#            sys.stderr.write("{}: {}\n".format(subitem, new_items[item][subitem]))
            new_doc = {}
            new_doc[subitem] = {}
            new_doc[subitem]['@rdf:about'] = new_items[item][subitem]
            new_doc[subitem]['schema:title'] = subitem
            result['rdf:RDF']['rdf:Description'].append(new_doc.pop(subitem))


    uitvoer = open(outputfile,"w", encoding='utf-8')
    xmltodict.unparse(result, output=uitvoer, pretty=True)

    Misc.einde()

