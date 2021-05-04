from bs4 import BeautifulSoup
import requests
import warnings
warnings.filterwarnings('ignore')

class Course():
    def get_course(self,inputted):
        catoid, coid = inputted[0], inputted[1]
        url = f"https://academiccalendars.romcmaster.ca/preview_course_nopop.php?catoid={catoid}&coid={coid}"
        r = requests.get(url,verify=False)
        data = BeautifulSoup(r.text,"html.parser")
        stuff = data.find_all("p")
        content = data.find("p")
        identifiers = ["Prerequisite", "Co-requisite", "Antirequisite", "Cross-list"]
        has_terms = True
        for items in stuff:
            if " term" in items.text:
                content = items
                break
        else:
            has_terms = False
            for identifier in identifiers:
                if identifier in items.text:
                    content = items
                    break

        course_name = content.h1.text.strip()
        unit_count = int(str(content.text)[str(content.text).index("unit")-3:str(content.text).index("unit")-1])
        new_cont = str(content)[str(content).index("unit(s)")+18:]
        course_desc = new_cont[:str(new_cont).index("<br/>")]
        if "<a href" in course_desc:
            course_desc = content.text[content.text.index("unit(s)")+8:content.text.index(course_desc[-10:])+10]
        new_cont = new_cont[new_cont.index("<br/>")+5:]
        hours = ""
        if has_terms:
            hours = new_cont[:new_cont.index("<br/>")]
        new_cont = new_cont[new_cont.index("<br/>")+5:]
        for ids in identifiers:
            try:
                reqs = content.text[content.text.index(ids):]
                break
            except:
                pass
        else:
            if "terms" in content.text:
                reqs = content.text[content.text.index("terms")+5:]
            else:
                reqs = content.text[content.text.index("term")+4:]

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
                break
        else:
            url = f"https://academiccalendars.romcmaster.ca/content.php?catoid=44&navoid=9045&filter%5B27%5D={dept}&filter%5Bcpage%5D=2"
            r = requests.get(url,verify=False)
            soup = BeautifulSoup(r.text,"html.parser")
            list_of_courses = soup.find_all("a", {"href": True, "target": "_blank", "aria-expanded": "false"})
            for course in list_of_courses:
                if course.text[:len(dept)+5] == query:
                    catoid = str(course)[str(course).index("catoid=")+7:str(course).index("catoid=")+9]
                    coid = str(course)[str(course).index("coid=")+5:str(course).index("coid=")+11]
                    course_list = [catoid,coid]
                    break

        try:
            x = self.get_course(course_list)
            return [x[0],str(x[1])+" unit(s)",x[2],x[3],x[4]]
        except:
            return "Error"

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
