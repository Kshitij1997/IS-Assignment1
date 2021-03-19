import csv
import json
import os
import urllib.parse
import pandas
import requests


def generate_topics():
    courses_dataframe = pandas.read_csv("datasets/courses.csv")
    topics_csv_exists = os.path.isfile('datasets/topics.csv')
    with open('datasets/topics.csv', 'a+', newline='') as topics_csv:
        topics_csv.seek(0)
        topics_csv_columns = ['Course ID', 'Topic Name', 'Topic Link']
        writer = csv.DictWriter(topics_csv, fieldnames=topics_csv_columns)
        if not topics_csv_exists:
            writer.writeheader()
        else:
            next(topics_csv)
        course_id_list = list()
        reader = csv.reader(topics_csv)
        for row in reader:
            course_id_list.append(row[0])
        for index, course in courses_dataframe.iterrows():
            course_id = course["Course ID"]
            if str(course_id) in course_id_list:
                continue
            course_name = course["Course Name"]
            course_description = course["Course Description"]
            data = str(course_name) + " " + str(course_description)
            try:
                base_url = 'http://localhost:2222/rest/annotate?text={text}&confidence={confidence}&support={support}'
                confidence = '0.9'
                support = '0'
                request = base_url.format(
                    text=urllib.parse.quote_plus(data),
                    confidence=confidence,
                    support=support
                )
                headers = {'Accept': 'application/json'}
                request = requests.get(url=request, headers=headers)
                response = json.loads(request.content)
                if 'Resources' in response:
                    topics_csv.seek(0, 2)
                    resources = response['Resources']
                    topics_list = list()
                    for resource in resources:
                        surface_form = resource['@surfaceForm']
                        if courses_dataframe['Course Subject'].str.contains(surface_form).any():
                            continue
                        uri = resource['@URI']
                        topic = dict()
                        topic['Course ID'] = course_id
                        topic['Topic Name'] = surface_form
                        topic['Topic Link'] = urllib.parse.quote_plus(uri)
                        topics_list.append(topic)
                    for topic in topics_list:
                        writer.writerow(topic)
            except json.JSONDecodeError:
                continue


def remove_duplicates():
    topics_dataframe = pandas.read_csv("datasets/topics.csv", encoding='ISO-8859-1')
    topics_dataframe.drop_duplicates(subset='Topic Name', keep='last')


if __name__ == "__main__":
    generate_topics()
    remove_duplicates()
