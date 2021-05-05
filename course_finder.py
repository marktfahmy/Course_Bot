import sqlite3
from sqlite3 import Error
from bs4 import BeautifulSoup
import requests
import warnings
warnings.filterwarnings('ignore')

db_file = "courses.db"

class Course():
    def find_course(self,course_code):
        conn = sqlite3.connect(db_file)
        dept, code = course_code.split()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {dept.upper()} WHERE ID = '{code.upper()}'")
        course = cur.fetchone()
        conn.close()
        return [course[0], str(course[1]) + " unit(s)", course[2], course[3], course[4]]

    def search_for_course(self,query):
        url = f"https://academiccalendars.romcmaster.ca/content.php?&filter%5Bkeyword%5D={query}&cur_cat_oid=44&navoid=9045"
        r = requests.get(url,verify=False)
        soup = BeautifulSoup(r.text,"html.parser")
        list_of_courses = soup.find_all("a", {"href": True, "target": "_blank", "aria-expanded": "false"})
        course_list = []
        for course in list_of_courses:
            name = course.text
            course_list.append(name)
        return course_list
