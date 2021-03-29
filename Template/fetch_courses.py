import pandas


# user = '349'
# key = '5d34b270604b1083d6d2bc4c40a693bb'
#
#
# def open_connection(username, password):
#     api_url = "https://opendata.concordia.ca"
#     password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
#     password_mgr.add_password(None, api_url, username, password)
#     handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
#     opener = urllib.request.build_opener(handler)
#     opener.open(api_url)
#     urllib.request.install_opener(opener)
#
#
# def make_request(url):
#     with urllib.request.urlopen(url) as req:
#         res = req.read()
#     return res
#
#
# def save_courses(courses_list):
#     courses_dataframe = pandas.DataFrame(courses_list)
#     courses_dataframe.drop(['career', 'classUnit', 'prerequisites', 'crosslisted'], axis=1, inplace=True)
#     courses_dataframe.to_csv(r'Dataset\courses.csv', header=True, index=False)


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
    # open_connection(user, key)
    # courses_list = list()
    # career_list = ['GRAD', 'UGRD']
    #
    # for career in career_list:
    #     catalog_response = make_request(f'https://opendata.concordia.ca/API/v1/course/catalog/filter/*/*/' + career)
    #     courses_list.extend(json.loads(catalog_response))
    #
    # count = 0
    # for i in range(0, len(courses_list) - 1):
    #     id_description_response = make_request(
    #         f'https://opendata.concordia.ca/API/v1/course/description/filter/' + courses_list[i]["ID"])
    #     id_description_list = json.loads(id_description_response)
    #     courses_list[i].update(id_description_list[0])
    #     del id_description_response
    #     del id_description_list
    #     count += 1
    #     if count % 1000 == 0:
    #         print(str(count) + " courses generated.")
    #
    # save_courses(courses_list)
