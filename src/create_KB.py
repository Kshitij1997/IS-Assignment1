# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 13:06:38 2021

@author: Piyush
"""
#import fetch
import os
import pandas
import urllib.parse
from rdflib import Namespace, Graph, RDF, RDFS, URIRef, Literal
from rdflib.namespace import FOAF, XSD, OWL

def code_url(url):
    return urllib.parse.unquote_plus(url)

#fetch.fetch_courses()
namespaces_dict = {"dbo": "http://dbpedia.org/ontology/",
                   "dbr": "http://dbpedia.org/resource/",
                   "sch": "http://example.org/schema#/"}

dbo = Namespace(namespaces_dict.get("dbo"))
dbr = Namespace(namespaces_dict.get("dbr"))
schema = Namespace(namespaces_dict.get("sch"))

graph = Graph()

graph.bind('dbo', dbo)
graph.bind('dbr', dbr)
graph.bind('sch', schema)
graph.bind('owl', OWL)
graph.bind('foaf', FOAF)
graph.bind('xsd', XSD)

Concordia_University = URIRef(schema.Concordia_University)

def add_university():
    graph.add((Concordia_University, RDF.type, schema.University))
    graph.add((Concordia_University, schema.uniName, Literal("Concordia University", lang="en")))
    graph.add((Concordia_University, RDFS.label, Literal("Concordia University", lang="en")))
    graph.add((Concordia_University, RDFS.comment, Literal("Concordia University is a university.", lang="en")))
    graph.add((Concordia_University,OWL.sameAs, URIRef(dbr.Concordia_University)))


def get_unique_subjects_from_dataset():
    courses_dataframe = pandas.read_csv('Dataset/courses.csv')
    return courses_dataframe['Course Subject'].drop_duplicates().values.tolist()


def get_courses_for_a_subject(subject):
    courses_dataframe = pandas.read_csv('Dataset/courses.csv')
    course_df = courses_dataframe[(courses_dataframe['Course Subject'] == subject)]
    return course_df



def add_subjectsWithCourses():
    subject_list = get_unique_subjects_from_dataset()
    for subject_name in subject_list:
        course_list = get_courses_for_a_subject(subject_name)
        for i in range(len(course_list)):
            add_courses(i, course_list,subject_name)
    graph.add((schema.COMP6741, RDFS.seeAlso,
               URIRef("https://moodle.concordia.ca/moodle/course/view.php?id=132738")))  

def add_courses(i, course_list, subject_name):
    course_number = str(course_list.iloc[i]['Course Number'])
    course_name = course_list.iloc[i]['Course Name']
    course_description = course_list.iloc[i]['Course Description']
    course = schema[subject_name+str(course_number)]
    graph.add((course, RDF.type, schema.Course))
    graph.add((course, schema.courseName, Literal(course_name, datatype=XSD.string)))
    graph.add((course, schema.subject, Literal(subject_name, datatype=XSD.string)))
    graph.add((course, schema.number, Literal(str(course_number), datatype=XSD.string)))
    graph.add((course,schema.courseDesc, Literal(course_description, datatype=XSD.string)))
    graph.add((course, RDFS.label, Literal(course_number, lang="en")))
    graph.add((course, RDFS.comment,
               Literal(course_number + " is a part of " + subject_name + ".", lang="en")))
   
    
   

def add_topics():
    topics=["Expert_System","Knowledge_Graphs","Computer"]
    course= URIRef("http://example.org/schema#/COMP6741")
    for t in topics:
        topic=schema[str(t)]
        graph.add((topic, RDF.type, schema.Topic))
        graph.add((topic, schema.topicName, Literal(t, datatype=XSD.string)))
        graph.add((topic, schema.coveredInCourse, course))
        graph.add((topic, OWL.sameAs, URIRef("http://dbpedia.org/resource/"+t)))

def add_lecture(c):
   cd=os.getcwd()
   cd=cd.replace(os.sep, '/')
   course_name=c
   course=URIRef("http://example.org/schema#/"+c)
   p="file:///"
   for roots, dirs1, files1 in os.walk(cd+"/Dataset/CoursesDataset/"+c+"/"):
        for file in files1:
            if "outline" in file:
                outline=URIRef(p+roots+file)
                graph.add((course, schema.outline, outline))
   for roots, dirs1, files1 in os.walk(cd+"/Dataset/CoursesDataset/"+c+"/lecture"):
        for d in dirs1:
            s=d.split(".")
            lecture_no=s[0]
            lecture_name=s[1]
            lecture=schema[str(course_name+"-l"+lecture_no)]
            graph.add((lecture, RDF.type, schema.lecture))
            graph.add((lecture, schema.forCourse, course))
            graph.add((lecture, schema.lectNumber, Literal(lecture_no, datatype=XSD.int)))
            
            topic=schema[str(lecture_name)]
            graph.add((topic, RDF.type, schema.Topic))
            graph.add((topic, schema.topicName, Literal(lecture_name, datatype=XSD.string)))
            graph.add((topic, schema.coveredInLecture, lecture))
            graph.add((topic, OWL.sameAs, URIRef("http://dbpedia.org/resource/"+lecture_name)))
            graph.add((lecture, schema.lectName, Literal(lecture_name, datatype=XSD.String)))
            content=schema[str(course_name+"content-lecture"+lecture_no)]
            graph.add((content, RDF.type, schema.lectContent))
            for root, dirs, files in os.walk(roots+"/"+d+"/"):
                for file in files:
                    path=(p+os.path.join(root, file))
                    s=URIRef(str(path))
                    if "slides" in file:                        
                        graph.add((s,RDF.type,schema.slide))
                        graph.add((content, schema.hasSlides,s))
                    elif "worksheet" in file:
                        graph.add((s,RDF.type,schema.worksheet))
                        graph.add((content, schema.hasWorksheets,s))
                    elif "readings" in file:
                        graph.add((s,RDF.type,schema.reading))
                        graph.add((content, schema.hasReadings, s))
                    elif "others" in file:
                        graph.add((s,RDF.type,schema.other))
                        graph.add((content, schema.hasOthers, s))
            graph.add((lecture, schema.hasContent,content))
    
               
           
            
def add_labs(c):
   cd=os.getcwd()
   cd=cd.replace(os.sep, '/')
   course_name=c
   p="file:///"
   for roots, dirs1, files1 in os.walk(cd+"/Dataset/CoursesDataset/"+c+"/labs"):
        for d in dirs1:
            s=d.split(".")
            lab_no=s[0]
            di=s[1].split("-")
            lab_name=di[0]
            lecture_no=di[1]
            lecture=URIRef("http://example.org/schema#/"+course_name+"-l"+lecture_no)
            lab=schema[str(c+"-lab"+lab_no)]
            graph.add((lab, RDF.type, schema.lab))
            graph.add((lab, RDFS.subClassOf, lecture))
            graph.add((lab, schema.labNumber, Literal(lab_no, datatype=XSD.int)))
            graph.add((lab, schema.labName, Literal(lab_name, datatype=XSD.int)))
            content=schema[str(course_name+"content-lab"+lab_no)]
            graph.add((content, RDF.type, schema.labContent))
            for root, dirs, files in os.walk(roots+"/"+d+"/"):
                for file in files:
                    path=(p+os.path.join(root, file))
                    s=URIRef(str(path))
                    if "slides" in file:                        
                        graph.add((s,RDF.type,schema.slide))
                        graph.add((content, schema.Slides,s))
                    elif "worksheet" in file:
                        graph.add((s,RDF.type,schema.worksheet))
                        graph.add((content, schema.Worksheets,s))
                    elif "readings" in file:
                        graph.add((s,RDF.type,schema.reading))
                        graph.add((content, schema.Readings, s))
                    elif "others" in file:
                        graph.add((s,RDF.type,schema.other))
                        graph.add((content, schema.Others, s))
            graph.add((lab, schema.Content,content))
            
            
def save_graph():
    graph.serialize(destination='KnowledgeBase.nt', format='nt')
    print("Knowledge Base saved as:"+os.getcwd()+"\KnowledgeBase.nt")


add_university()
add_subjectsWithCourses()
add_lecture("COMP6741")
add_lecture("SOEN6841")
add_labs("COMP6741")
add_labs("SOEN6841")
add_topics()
save_graph()
