import os
import random

import pandas


def get_student_ids():
    students_csv = pandas.read_csv('datasets/students.csv', index_col=False)
    return students_csv['Student ID'].values.tolist()


def get_course_ids():
    courses_csv = pandas.read_csv('datasets/courses.csv', index_col=False)
    return courses_csv['Course ID'].values.tolist()


def get_random_course_term():
    terms_list = ['Summer', 'Fall', 'Winter']
    years_list = ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']
    return str(terms_list[random.randint(0, len(terms_list) - 1)]) + " " + (
        years_list[random.randint(0, len(years_list) - 1)])


def get_random_course_grade():
    grades_list = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C', 'F']
    return str(grades_list[random.randint(0, len(grades_list) - 1)])


student_id_list = get_student_ids()
course_id_list = get_course_ids()
current_course_index = 0
student_course_records = list()
for student_id in student_id_list:
    course_count = random.randint(0, 5)
    for i in range(0, course_count - 1):
        record = dict()
        record['Course ID'] = course_id_list[current_course_index + i]
        record['Student ID'] = student_id
        record['Term'] = get_random_course_term()
        record['Grade'] = get_random_course_grade()
        student_course_records.append(record)
    current_course_index += course_count
    if current_course_index + 5 >= len(course_id_list):
        current_course_index = 0
pandas.DataFrame(student_course_records).to_csv('datasets/students_courses.csv', index=False)
