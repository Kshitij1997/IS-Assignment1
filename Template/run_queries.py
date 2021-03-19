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
                   "isd": "http://intelligent_system.io/data/",
                   "isdp": "http://intelligent_system.io/data/property/",
                   "schema": "http://schema.org/"}

queries_files_list = list()
get_queries_files()
graph = Graph()
graph.parse("rdf/graph.rdf", format="turtle")
for query_file in queries_files_list:
    print("Running query: " + str(query_file))
    query_str = get_query_from_file()
    query = prepareQuery(query_str,
                         initNs={"rdf": RDF, "rdfs": RDFS, "xsd": XSD, "dbo": namespaces_dict.get("dbo"),
                                 "dbr": namespaces_dict.get("dbr"), "isd": namespaces_dict.get("isd"),
                                 "isdp": namespaces_dict.get("isdp"), "schema": namespaces_dict.get("schema"),
                                 "owl": OWL, "foaf": FOAF, "dc": DC})
    result = graph.query(query)
    for row in result:
        print(row)
