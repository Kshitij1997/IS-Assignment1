import pandas
import urllib.parse
from rdflib import Namespace, Graph, RDF, RDFS, URIRef, Literal, BNode
from rdflib.namespace import FOAF, DC, XSD, OWL


def encode_url(url):
    return urllib.parse.quote_plus(url)


namespaces_dict = {"dbo": "http://dbpedia.org/ontology/",
                   "dbr": "http://dbpedia.org/resource/",
                   "isd": "http://intelligent_system.io/data/",
                   "isdp": "http://intelligent_system.io/data/property/",
                   "schema": "http://schema.org/"}

dbo = Namespace(namespaces_dict.get("dbo"))
dbr = Namespace(namespaces_dict.get("dbr"))
isd = Namespace(namespaces_dict.get("isd"))
isdp = Namespace(namespaces_dict.get("isdp"))
schema = Namespace(namespaces_dict.get("schema"))

graph = Graph()

graph.bind('dbo', dbo)
graph.bind('dbr', dbr)
graph.bind('isd', isd)
graph.bind('isdp', isdp)
graph.bind('schema', schema)
graph.bind('owl', OWL)
graph.bind('foaf', FOAF)
graph.bind('dc', DC)
graph.bind('xsd', XSD)

Concordia_University = URIRef(isd.Concordia_University + '/')
Subject = isd.Subject
Course = isd.Course
Topic = isd.Topic
Student = isd.Student


def add_university():
    graph.add((dbo.University, RDF.type, RDFS.Class))
    graph.add((dbo.University, RDFS.subClassOf, FOAF.Organization))
    graph.add((Concordia_University, RDF.type, dbo.University))
    graph.add((Concordia_University, RDFS.label, Literal("Concordia University", lang="en")))
    graph.add((Concordia_University, RDFS.comment, Literal("Concordia University is a university.", lang="en")))
    graph.add((Concordia_University, RDFS.seeAlso, URIRef("http://www.concordia.ca/")))
    graph.add((Concordia_University, OWL.sameAs, URIRef(dbr.Concordia_University)))


def get_unique_subjects_from_dataset():
    courses_dataframe = pandas.read_csv('datasets/courses.csv')
    return courses_dataframe['Course Subject'].drop_duplicates().values.tolist()


def get_courses_for_a_subject(subject):
    courses_dataframe = pandas.read_csv('datasets/courses.csv')
    course_df = courses_dataframe[(courses_dataframe['Course Subject'] == subject)]
    return course_df


def get_topics_for_a_course(course_id):
    topics_dataframe = pandas.read_csv('datasets/topics.csv', encoding='ISO-8859-1')
    return topics_dataframe[(topics_dataframe['Course ID'] == course_id)]


def get_students_with_a_course(course_id):
    student_course_dataframe = pandas.read_csv('datasets/students_courses.csv')
    return student_course_dataframe[(student_course_dataframe['Course ID'] == course_id)]


def get_student_details(student_id):
    student_dataframe = pandas.read_csv('datasets/students.csv')
    return student_dataframe[(student_dataframe['Student ID'] == student_id)].to_dict('records')


def add_subjects():
    graph.add((isd.Subject, RDF.type, RDFS.Class))
    graph.add((isd.Course, RDF.type, RDFS.Class))
    subject_list = get_unique_subjects_from_dataset()
    for subject_name in subject_list:
        subject = isd[subject_name + '/']
        graph.add((subject, RDF.type, isd.Subject))
        graph.add((subject, RDFS.label, Literal(subject_name, lang="en")))
        graph.add((subject, FOAF.name, Literal(subject_name, datatype=XSD.string)))
        graph.add((subject, RDFS.comment,
                   Literal(subject_name + " is a subject taught at Concordia University.", lang="en")))
        graph.add((subject, schema.isPartOf, Concordia_University))
        course_list = get_courses_for_a_subject(subject_name)
        for i in range(len(course_list)):
            add_courses(i, course_list, subject, subject_name)


def add_courses(i, course_list, subject, subject_name):
    course_number = str(course_list.iloc[i]['Course Number'])
    course_name = course_list.iloc[i]['Course Name']
    course_id = course_list.iloc[i]['Course ID']
    course_description = course_list.iloc[i]['Course Description']
    course = isd[str(course_id) + '/']
    graph.add((subject, schema.hasPart, course))
    graph.add((course, RDF.type, isd.Course))
    graph.add((course, schema.isPartOf, subject))
    graph.add((course, RDFS.label, Literal(course_number, lang="en")))
    graph.add((course, RDFS.comment,
               Literal(course_number + " is a part of " + subject_name + ".", lang="en")))
    graph.add((course, RDFS.seeAlso,
               URIRef("https://opendata.concordia.ca/datasets/sis/CU_SR_OPEN_DATA_CATALOG.csv")))
    graph.add((course, FOAF.name, Literal(course_name, datatype=XSD.string)))
    graph.add((course, DC.identifier, Literal(str(course_id), datatype=XSD.string)))
    graph.add((course, isdp.Number, Literal(course_number, datatype=XSD.string)))
    graph.add((course, DC.description, Literal(course_description, datatype=XSD.string)))
    topic_list = get_topics_for_a_course(course_id)
    for j in range(len(topic_list)):
        add_topics(j, topic_list, course, subject)
    student_course_list = get_students_with_a_course(course_id)
    for k in range(len(student_course_list)):
        add_students(k, student_course_list, course, subject)


def add_topics(j, topic_list, course, subject):
    topic_name_str = topic_list.iloc[j]['Topic Name']
    topic_name = topic_name_str.replace(" ", "_")
    topic_link = topic_list.iloc[j]['Topic Link']
    topic_link = urllib.parse.unquote_plus(topic_link)
    topic = isd[topic_name + '/']
    graph.add((course, schema.hasPart, topic))
    graph.add((topic, RDF.type, isd.Topic))
    graph.add((topic, RDFS.label, Literal(topic_name_str, lang="en")))
    graph.add((topic, RDFS.comment,
               Literal(topic_name_str + " topic included in the course.", lang="en")))
    graph.add((topic, OWL.sameAs, URIRef(topic_link)))
    graph.add((topic, schema.isPartOf, course))
    graph.add((topic, DC.subject, subject))


def add_students(k, student_course_list, course, subject):
    student_id = student_course_list.iloc[k]['Student ID']
    student = isd[str(student_id) + '/']
    student_dict = get_student_details(student_id)[0]
    student_family_name = student_dict.get('Family Name')
    student_given_name = student_dict.get('Given Name')
    student_email = student_dict.get('Email')
    graph.add((student, schema.memberOf, Concordia_University))
    graph.add((student, RDF.type, isd.Student))
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
    graph.add((student, isdp.has, blank))
    graph.add((blank, schema.isPartOf, course))
    graph.add((blank, DC.subject, subject))
    graph.add((blank, isdp.hasGrade, Literal(student_course_list.iloc[k]['Grade'], datatype=XSD.string)))
    graph.add((blank, isdp.inTerm, Literal(student_course_list.iloc[k]['Term'], datatype=XSD.string)))


def save_graph():
    graph.serialize(destination='rdf/graph.rdf', format='turtle')


add_university()
add_subjects()
save_graph()
