import sqlite3
from sqlite3 import Error
from bs4 import BeautifulSoup
import requests
import warnings
warnings.filterwarnings('ignore')

db_file = "courses.db"

pseudonyms = {'ANTHROPOLOGY': 'ANTHROP',
 'ART HISTORY': 'ARTHIST',
 'ARTS & SCIENCE': 'ARTSSCI',
 'ASTRONOMY': 'ASTRON',
 'AUTOMOTIVE & VEHICLE TECH': 'AUTOTECH',
 'BIOCHEMISTRY': 'BIOCHEM',
 'BIOMEDICAL DISCOVERY & COMMERCIALIZATION': 'BIOMEDDC',
 'BIOPHYSICS': 'BIOPHYS',
 'BIOSAFETY': 'BIOSAFE',
 'BIOTECHNOLOGY': 'BIOTECH',
 'CHEMICAL BIOLOGY': 'CHEMBIO',
 'CHEMICAL': 'CHEMENG',
 'CHEMICAL ENGINEERING': 'CHEMENG',
 'CHEMISTRY': 'CHEM',
 'CIVIL ENG INFRASTRUCTURE TECH': 'CIVTECH',
 'CIVIL': 'CIVENG',
 'CIVIL ENGINEERING': 'CIVENG',
 'CLASSICS': 'CLASSICS',
 'COLLABORATIVE': 'COLLAB',
 'COMMERCE': 'COMMERCE',
 'COMMUNICATION STUDIES': 'CMST',
 'COMMUNITY ENGAGEMENT': 'CMTYENGA',
 'COMPUTER ENGINEERING': 'COMPENG',
 'COMPUTER SCIENCE': 'COMPSCI',
 'EARTH SCIENCES': 'EARTHSC',
 'ECONOMICS': 'ECON',
 'ELECTRICAL': 'ELECENG',
 'ELECTRICAL ENGINEERING': 'ELECENG',
 'ENERGY ENGINEERING TECH': 'ENRTECH',
 'ENGINEERING': 'ENGINEER',
 'ENGINEERING & MANAGEMENT PROGRAM': 'ENGNMGT',
 'ENGINEERING & SOCIETY PROGRAM': 'ENGSOCTY',
 'ENGINEERING PHYSICS': 'ENGPHYS',
 'ENGINEERING TECHNOLOGY': 'ENGTECH',
 'ENVIRONMENT & SOCIETY': 'ENVSOCTY',
 'ENVIRONMENTAL SCIENCE': 'ENVIRSC',
 'EXPLORE (INTERDISCIPLINARY EXPERIENCES)': 'EXPLORE',
 'GENDER STUDIES': 'GENDRST',
 'GENERAL TECHNOLOGY': 'GENTECH',
 'GLOBAL PEACE & SOCIAL JUSTICE': 'PEACJUST',
 'GLOBALIZATION STUDIES': 'GLOBALZN',
 'HEALTH SCIENCES': 'HTHSCI',
 'HEALTH, AGING & SOCIETY': 'HLTHAGE',
 'HEBREW': 'HEBREW',
 'HISTORY': 'HISTORY',
 'HUMAN BEHAVIOUR': 'HUMBEHV',
 'HUMANITIES': 'HUMAN',
 'INDIGENOUS STUDIES': 'INDIGST',
 'INNOVATION': 'INNOVATE',
 'INSPIRE (INTERSESSION)': 'INSPIRE',
 'INTEGRATED BIOMEDICAL ENGINEERING & HEALTH SCIENCES': 'IBEHS',
 'IBIOMED': 'IBEHS',
 'IBIO': 'IBEHS',
 'INTEGRATED BUSINESS & HUMANITIES': 'IBH',
 'INTEGRATED SCIENCE': 'ISCI',
 'INTERNATIONAL ENGAGEMENT': 'INTENG',
 'INUKTITUT': 'INUKTUT',
 'KINESIOLOGY': 'KINESIOL',
 'LABOUR STUDIES': 'LABRST',
 'LIFE SCIENCES': 'LIFESCI',
 'LINGUISTICS': 'LINGUIST',
 'MANUFACTURING TECHNOLOGY': 'MANTECH',
 'MATERIALS': 'MATLS',
 'MSE': 'MATLS',
 'MATERIALS SCIENCE & ENGINEERING': 'MATLS',
 'MATERIALS ENGINEERING': 'MATLS',
 'MATHEMATICS': 'MATH',
 'MCMASTER ENGLISH LANGUAGE DEVELOPMENT': 'MELD',
 'MECHANICAL': 'MECHENG',
 'MECHANICAL ENGINEERING': 'MECHENG',
 'MECHATRONICS': 'MECHTRON',
 'MECHATRONICS ENGINEERING': 'MECHTRON',
 'MEDIA ARTS': 'MEDIAART',
 'MEDICAL PHYSICS': 'MEDPHYS',
 'MEDICAL RADIATION SCIENCES': 'MEDRADSC',
 'MIDWIFERY': 'MIDWIF',
 'MOLECULAR BIOLOGY': 'MOLBIOL',
 'MUSIC COGNITION': 'MUSICCOG',
 'NEUROSCIENCE': 'NEUROSCI',
 'NURSING': 'NURSING',
 'OJIBWE': 'OJIBWE',
 'PHARMACOLOGY': 'PHARMAC',
 'PHILOSOPHY': 'PHILOS',
 'POLISCI': 'POLSCI',
 'POLITICAL SCIENCE': 'POLSCI',
 'PROCESS AUTOMATION TECHNOLOGY': 'PROCTECH',
 'PSYCHOLOGY': 'PSYCH',
 'PSYCHOLOGY, NEUROSCIENCE & BEHAVIOUR': 'PNB',
 'SCHOOL FOR ENG PRACTICE': 'SEP',
 'SCIENCE COMMUNICATION': 'SCICOMM',
 'SMART ENGINEERING TECHNOLOGY': 'SMRTTECH',
 'SOCIAL PSYCHOLOGY': 'SOCPSY',
 'SOCIAL SCIENCES': 'SOCSCI',
 'SOCIAL WORK': 'SOCWORK',
 'SOCIETY, CULTURE, & RELIGION': 'SCAR',
 'SOCIOLOGY': 'SOCIOL',
 'SOFTWARE ENGINEERING': 'SFWRENG',
 'SOFTWARE ENGINEERING TECHNOLOGY': 'SFWRTECH',
 'SPANISH': 'SPANISH',
 'STATISTICS': 'STATS',
 'SUSTAINABILITY': 'SUSTAIN',
 'THEATRE & FILM': 'THTRFLM'}

class Course():
    def find_course(self, course_dept, course_code):
        conn = sqlite3.connect(db_file)
        try:
            if (course_dept not in pseudonyms.values()) and (course_dept.replace("AND","&") in pseudonyms.keys()):
                course_dept = pseudonyms[course_dept.replace("AND","&")]
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM '{course_dept}' WHERE ID = '{course_code}'")
            course = cur.fetchone()
            if course == None:
                return "Error"
        except Error as e:
            print(e)
            return "Error"
        conn.close()
        return [course[0], str(course[1]) + " unit(s)", course[2], course[3], course[4]]

    def search_for_course(self, query):
        url = "https://academiccalendars.romcmaster.ca/content.php?&filter%5Bkeyword%5D=\"" + '+'.join(query) + "\"&cur_cat_oid=44&navoid=9045"
        r = requests.get(url,verify=False)
        soup = BeautifulSoup(r.text,"html.parser")
        list_of_courses = soup.find_all("a", {"href": True, "target": "_blank", "aria-expanded": "false"})
        course_list = []
        for course in list_of_courses:
            name = course.text
            course_list.append(name)
        return course_list



