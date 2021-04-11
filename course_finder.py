from bs4 import BeautifulSoup
import requests
import warnings
warnings.filterwarnings('ignore')

class Course():
    def __init__(self):
        pass

    def get_course(self,inputted):
        catoid, coid = inputted[0], inputted[1]
        url = f"https://academiccalendars.romcmaster.ca/preview_course_nopop.php?catoid={catoid}&coid={coid}"
        r = requests.get(url,verify=False)
        data = BeautifulSoup(r.text,"html.parser")
        stuff = data.find_all("p")
        content = data.find("p")
        for items in stuff:
            if "Prerequisite" in items.text:
                content = items

        course_name = content.h1.text.strip()
        unit_count = int(str(content.text)[str(content.text).index("unit")-3:str(content.text).index("unit")-1])
        course_desc = content.text[content.text.index("unit(s)")+7:content.text.index("\n")].strip()
        content = content.text[content.text.index("\n")+1:]
        hours = content[:content.index("\n")]
        reqs = content[content.index("\n")+1:]
        return [course_name,unit_count,course_desc,hours,reqs]

    def find_course(self,course_code):
        query = course_code.upper()
        dept = query.split()[0]
        url = f"https://academiccalendars.romcmaster.ca/content.php?filter%5B27%5D={dept}&cur_cat_oid=44&navoid=9045"
        r = requests.get(url,verify=False)
        soup = BeautifulSoup(r.text,"html.parser")
        list_of_courses = soup.find_all("a", {"href": True, "target": "_blank", "aria-expanded": "false"})
        for course in list_of_courses:
            if course.text[:len(dept)+5] == query:
                catoid = str(course)[str(course).index("catoid=")+7:str(course).index("catoid=")+9]
                coid = str(course)[str(course).index("coid=")+5:str(course).index("coid=")+11]
                course_list = [catoid,coid]
        
        try:
            x = self.get_course(course_list)
            return [x[0],str(x[1])+" unit(s)","Description: "+x[2],x[3],x[4]]
        except:
            return "Error"

    def list_all_courses(self,dept):
        dept = dept.strip().upper()
        url = f"https://academiccalendars.romcmaster.ca/content.php?filter%5B27%5D={dept}&cur_cat_oid=44&navoid=9045"
        r = requests.get(url,verify=False)
        soup = BeautifulSoup(r.text,"html.parser")
        list_of_courses = soup.find_all("a", {"href": True, "target": "_blank", "aria-expanded": "false"})
        course_list = []
        for course in list_of_courses:
            name = course.text
            course_list.append(name)
        return course_list
