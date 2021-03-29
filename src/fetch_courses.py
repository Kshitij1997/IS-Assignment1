# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 13:38:24 2021

@author: Piyush
"""

import pandas



def fetch_courses():
    catalogs_csv = pandas.read_csv("https://opendata.concordia.ca/datasets/sis/CU_SR_OPEN_DATA_CATALOG.csv",
                                   engine="python")
    descriptions_csv = pandas.read_csv("https://opendata.concordia.ca/datasets/sis/CU_SR_OPEN_DATA_CATALOG_DESC.csv",
                                       engine="python")
    courses_dataframe = catalogs_csv.merge(descriptions_csv, on='Course ID')
    courses_dataframe.drop(
        courses_dataframe[~(courses_dataframe["Component Descr"] == "Lecture")].index,
        inplace=True)
    courses_dataframe.drop_duplicates(subset='Course ID', inplace=True)
    courses_dataframe.drop(
        ['Career', 'Class Units', 'Component Code', 'Component Descr', 'Pre Requisite Description',
         'Equivalent Courses'], axis=1,
        inplace=True)
    courses_dataframe.rename(
        columns={'Subject': 'Course Subject', 'Catalog': 'Course Number', 'Long Title': 'Course Name',
                 'Descr': 'Course Description'}, inplace=True)
    courses_dataframe.to_csv(r'Dataset\courses.csv', header=True, index=False)


if __name__ == "__main__":
    fetch_courses()
