# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 23:16:22 2021

@author: Piyush
"""

import os
from fnmatch import fnmatch
from rdflib import Graph
from rdflib.namespace import FOAF, DC, OWL, RDF, RDFS, XSD
from rdflib.plugins.sparql import prepareQuery


def get_queries_files():
    for root, dirs, files in os.walk("queries/"):
        for file in files:
            if file.endswith(".txt") | file.endswith(".TXT"):
                if not fnmatch(file, '*out*'):
                    queries_files_list.append(os.path.join(root, file))



def get_query_from_file():
    with open(query_file, 'r') as file:
        return file.read()


namespaces_dict = {"dbo": "http://dbpedia.org/ontology/",
                   "dbr": "http://dbpedia.org/resource/",
                   "schema": "http://example.org/schema#/"}

queries_files_list = list()
get_queries_files()
graph = Graph()
graph.parse("KnowledgeBase.nt", format="nt")
for query_file in queries_files_list:
    print("\n\n----------Running query: " + str(query_file))
    query_str = get_query_from_file()
    query = prepareQuery(query_str,
                         initNs={"rdf": RDF, "rdfs": RDFS, "xsd": XSD, "dbo": namespaces_dict.get("dbo"),
                               "sch": namespaces_dict.get("schema"), "dc": DC})
    result = graph.query(query)
    for row in result:
        print(row)
