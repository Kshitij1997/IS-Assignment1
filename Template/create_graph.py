import urllib.parse

import pandas
from rdflib import Namespace, Graph, RDF, RDFS, URIRef, Literal, BNode
from rdflib.namespace import FOAF, DC, XSD, OWL


def create_base_graph():
    # University = URIRef(University)
    # Concordia_University = URIRef(Concordia_University)
    # g.parse(source='rdf/rdf_schema.ttl', format="ttl")

    graph.add((ISDP.has, RDF.type, RDF.Property))
    graph.add((ISDP.has, RDFS.label, Literal("Has", lang="en")))
    graph.add((ISDP.has, RDFS.comment, Literal("Has is a property.", lang="en")))
    graph.add((ISDP.Number, RDF.type, RDF.Property))
    graph.add((ISDP.Number, RDFS.label, Literal("Course number", lang="en")))
    graph.add((ISDP.Number, RDFS.comment, Literal("Course number is a property.", lang="en")))
    graph.add((ISDP.Number, RDFS.domain, ISD.Course))
    graph.add((ISDP.Number, RDFS.range, ISD.Subject))

    graph.add((University, RDF.type, RDFS.Class))
    graph.add((ISD.Subject, RDF.type, RDFS.Class))
    graph.add((ISD.Course, RDF.type, RDFS.Class))
    graph.add((ISD.Topic, RDF.type, RDFS.Class))
    graph.add((ISD.Student, RDF.type, RDFS.Class))

    graph.add((University, RDFS.subClassOf, FOAF.Organization))
    graph.add((ISD.Course, RDFS.subClassOf, ISD.Subject))
    graph.add((ISD.Topic, RDFS.subClassOf, ISD.Course))
    graph.add((ISD.Student, RDFS.subClassOf, FOAF.Person))

    graph.add((Concordia_University, RDF.type, University))
    graph.add((Concordia_University, RDFS.label, Literal("Concordia University", lang="en")))
    graph.add((Concordia_University, RDFS.comment, Literal("Concordia University is a university.", lang="en")))
    graph.add((Concordia_University, RDFS.seeAlso, URIRef("http://www.concordia.ca/")))
    graph.add((Concordia_University, OWL.sameAs, URIRef(DBR.Concordia_University)))
    graph.add((Concordia_University, SCHEMA.hasPart, ISD.Subject))
    graph.add((Concordia_University, SCHEMA.member, ISD.Student))

    # graph.add((ISD.Subject, ISDR.has, ISD.Course))
    # graph.add((ISD.Course, ISDR.has, ISD.Topic))
    # graph.add((ISD.Student, ISDR.has, ISD.Course))
    #
    # graph.add((ISD.Subject, RDFS.subClassOf, Concordia_University))
    # graph.add((ISD.Subject, RDFS.label, Literal("Subject", lang="en")))
    # graph.add((ISD.Subject, RDFS.comment, Literal("Subject is a program annotation taught at the University.", lang="en")))
    #
    # graph.add((ISD.Student, RDFS.label, Literal("Student", lang="en")))
    # graph.add((ISD.Student, RDFS.comment, Literal("Student studies at Concordia University.", lang="en")))
    #
    # graph.add((ISD.Course, RDFS.subClassOf, ISD.Subject))
    # graph.add((ISD.Course, RDFS.label, Literal("Course", lang="en")))
    # graph.add((ISD.Course, RDFS.comment, Literal("Course is a part of subject.", lang="en")))
    # graph.add((ISD.Course, RDFS.seeAlso, URIRef("https://opendata.concordia.ca/datasets/sis/CU_SR_OPEN_DATA_CATALOG.csv")))
    #
    # graph.add((ISD.Topic, RDFS.label, Literal("Topic", lang="en")))
    # graph.add((ISD.Topic, RDFS.comment, Literal("Topic included in the course.", lang="en")))
    # graph.add((ISD.Topic, RDFS.domain, ISD.Course))
    # graph.add((ISD.Topic, RDFS.range, Concordia_University))


def get_unique_subjects():
    courses_dataframe = pandas.read_csv('datasets/courses.csv')
    return courses_dataframe['Course Subject'].drop_duplicates().values.tolist()


def get_courses_for_a_subject(subject):
    courses_dataframe = pandas.read_csv('datasets/courses.csv')
    return courses_dataframe[(courses_dataframe['Course Subject'] == subject)]


def get_topics_for_a_course(course_id):
    topics_dataframe = pandas.read_csv('datasets/topics.csv')
    return topics_dataframe[(topics_dataframe['Course ID'] == course_id)]


def get_students_with_a_course(course_id):
    student_course_dataframe = pandas.read_csv('datasets/students_courses.csv')
    return student_course_dataframe[(student_course_dataframe['Course ID'] == course_id)]


def get_student_details(student_id):
    student_dataframe = pandas.read_csv('datasets/students.csv')
    return student_dataframe[(student_dataframe['Student ID'] == student_id)].to_dict('records')


def add_courses():
    subject_list = get_unique_subjects()
    for subject_name in subject_list:
        subject = ISD[subject_name]
        graph.add((subject, RDF.type, ISD.Subject))
        graph.add((subject, RDFS.label, Literal(subject_name, lang="en")))
        graph.add((subject, RDFS.comment,
               Literal(subject_name + " is a program taught at Concordia University.", lang="en")))
        graph.add((subject, SCHEMA.isPartOf, Concordia_University))
        course_list = get_courses_for_a_subject(subject_name)
        for i in range(len(course_list)):
            course_number = course_list.iloc[i]['Course Number']
            course = ISD[course_number]
            graph.add((subject, SCHEMA.hasPart, course))
            graph.add((course, RDF.type, ISD.Course))
            graph.add((course, SCHEMA.isPartOf, subject))
            graph.add((course, RDFS.label, Literal(str(course_number), lang="en")))
            graph.add((course, RDFS.comment,
                   Literal(str(course_number) + " is a part of " + subject_name + ".", lang="en")))
            graph.add((course, RDFS.seeAlso,
                   URIRef("https://opendata.concordia.ca/datasets/sis/CU_SR_OPEN_DATA_CATALOG.csv")))
            graph.add((course, FOAF.name, Literal(course_list.iloc[i]['Course Name'], datatype=XSD.string)))
            graph.add((course, DC.identifier, Literal(course_list.iloc[i]['Course ID'], datatype=XSD.string)))
            graph.add((course, ISDP.Number, Literal(str(course_number), datatype=XSD.string)))
            graph.add((course, DC.description, Literal(course_list.iloc[i]['Course Description'], datatype=XSD.string)))
            course_id = course_list.iloc[i]['Course ID']
            topic_list = get_topics_for_a_course(course_id)
            for j in range(len(topic_list)):
                topic_name_str = topic_list.iloc[j]['Topic Name']
                topic_name = topic_name_str.replace(" ", "_")
                topic_link = topic_list.iloc[j]['Topic Link']
                topic_link = urllib.parse.unquote_plus(topic_link)
                topic = ISD[topic_name]
                graph.add((course, SCHEMA.hasPart, topic))
                graph.add((topic, RDF.type, ISD.Topic))
                graph.add((topic, RDFS.label, Literal(topic_name_str, lang="en")))
                graph.add((topic, RDFS.comment,
                       Literal(topic_name_str + " topic included in the course.", lang="en")))
                graph.add((topic, OWL.sameAs, URIRef(topic_link)))
                graph.add((topic, SCHEMA.isPartOf, course))
                graph.add((topic, DC.subject, subject))
            student_course_list = get_students_with_a_course(course_id)
            for k in range(len(student_course_list)):
                student_id = student_course_list.iloc[k]['Student ID']
                student = ISD[str(student_id)]
                student_dict = get_student_details(student_id)[0]
                student_family_name = student_dict.get('Family Name')
                student_given_name = student_dict.get('Given Name')
                student_email = student_dict.get('Email')
                graph.add((student, SCHEMA.memberOf, Concordia_University))
                graph.add((student, RDF.type, ISD.Student))
                graph.add((student, RDFS.label,
                       Literal(student_given_name + " " + student_family_name, lang="en")))
                graph.add((student, RDFS.comment,
                       Literal(student_given_name + " " + student_family_name + " studies at Concordia University.",
                               lang="en")))
                graph.add((student, DC.identifier, Literal(student_id, datatype=XSD.integer)))
                graph.add((student, FOAF.familyName, Literal(student_family_name, datatype=XSD.string)))
                graph.add((student, FOAF.givenName, Literal(student_given_name, datatype=XSD.string)))
                graph.add((student, FOAF.mbox, Literal(student_email, datatype=XSD.string)))
                blank = BNode()
                graph.add((student, ISDP.has, blank))
                graph.add((blank, SCHEMA.isPartOf, course))
                graph.add((blank, DC.subject, subject))
                graph.add((blank, ISDP.hasGrade, Literal(student_course_list.iloc[k]['Grade'], datatype=XSD.string)))
                graph.add((blank, ISDP.inTerm, Literal(student_course_list.iloc[k]['Term'], datatype=XSD.string)))


def save_graph():
    graph.serialize(destination='rdf/graph.rdf', format='turtle')


namespaces_dict = {"DBO": "http://dbpedia.org/ontology/",
                   "DBR": "http://dbpedia.org/resource/",
                   "ISD": "http://intelligent_system.io/data/",
                   "ISDP": "http://intelligent_system.io/data/property/",
                   "SCHEMA": "https://schema.org/"}

DBO = Namespace(namespaces_dict.get("DBO"))
DBR = Namespace(namespaces_dict.get("DBR"))
ISD = Namespace(namespaces_dict.get("ISD"))
ISDP = Namespace(namespaces_dict.get("ISDP"))
SCHEMA = Namespace(namespaces_dict.get("SCHEMA"))

graph = Graph()

graph.bind('DBO', DBO)
graph.bind('DBR', DBR)
graph.bind('ISD', ISD)
graph.bind('ISDP', ISDP)
graph.bind('SCHEMA', SCHEMA)
graph.bind('OWL', OWL)
graph.bind('FOAF', FOAF)
graph.bind('DC', DC)

University = DBO.University
Concordia_University = ISD.Concordia_University

create_base_graph()
add_courses()

save_graph()
