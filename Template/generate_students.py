# id, givenName, familyName, email
import pandas
from random import randint
import re


def get_student_name():
    names_file_csv = pandas.read_csv('datasets/random_names.csv', index_col=False)
    random_number = randint(1, 9999)
    scraped_name = str(names_file_csv['first_name'][random_number]) + " " + str(
        names_file_csv['last_name'][random_number])
    return scraped_name


def generate_random_id(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    random_student_id = randint(range_start, range_end)
    return random_student_id


def get_student_email(student_name):
    student_email = re.sub(r"[^\w\s]", '', student_name.lower())
    student_email = re.sub(r"\s+", '_', student_email)
    student_email = student_email + "@encs.concordia.ca"
    return student_email


def create_students():
    student_ids_list = list()
    student_first_names_list = list()
    student_last_names_list = list()
    student_emails_list = list()
    for i in range(0, 9999):
        student_id = generate_random_id(8)
        while student_id in student_ids_list:
            student_id = generate_random_id(8)
        student_ids_list.append(student_id)
        student_name = get_student_name()
        student_first_names_list.append(student_name.split(" ", 1)[0])
        student_last_names_list.append(student_name.split(" ", 1)[1])
        student_email = get_student_email(student_name)
        student_emails_list.append(student_email)
    students_dict = {'Student ID': student_ids_list, 'Given Name': student_first_names_list,
                     'Family Name': student_last_names_list, 'Email': student_emails_list}
    students_dataframe = pandas.DataFrame(students_dict)
    students_dataframe.to_csv('Dataset/students.csv', index=False)


create_students()
