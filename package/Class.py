from package import Section
from selenium import webdriver

class AClass:
    """A class for classes"""

    def __init__(self, subject, number):
        self.subject = subject
        self.number = number
        self.ccn = ""
        self.days = []
        self.lecture_start_time = ""
        self.lecture_end_time = ""
        self.location = ""
        self.instructor = ""
        self.discussions = []
        self.labs = []
        self.numEnrolled = 0
        self.size = 0

    def __str__(self):
        return self.subject + " " + str(self.number)

    def add_discussion(self, dis):
        self.discussions.append(dis)

    def add_lab(self, lab):
        self.labs.append(lab)

    def collect_data(self, driver):
        driver.get(
            "https://bcsweb.is.berkeley.edu/psc/bcsprd_pub/EMPLOYEE/HRMS/c/COMMUNITY_ACCESS.CLASS_SEARCH.GBL?ucFrom=berkeley")
        driver.find_element_by_name('SSR_CLSRCH_WRK_SUBJECT_SRCH$0').send_keys(self.subject)
        driver.find_element_by_name('SSR_CLSRCH_WRK_CATALOG_NBR$1').send_keys(str(self.number))
        driver.find_element_by_name('CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH').click()
        driver.implicitly_wait(100)

        classesText = driver.find_element_by_class_name("SSSGROUPBOX").text
        parts = classesText.split(" ")
        numberOfClasses = int(parts[0].encode('utf-8'))
        class_format = ""  # LEC, DIS, LAB, etc.

        # find class / section / dayTime / room / instructor / dateOfClass / status
        for i in range(numberOfClasses):
            # find class
            classNum = driver.find_element_by_name('MTG_CLASS_NBR$' + str(i)).text

            # find section
            sectionNum = driver.find_element_by_name('MTG_CLASSNAME$' + str(i)).text
            # sectionParts = sectionText.split(' ')
            # sectionNum = sectionParts[0]
            class_format = sectionNum.split("-", 1)[1].encode('utf-8')

            # find dayTime
            dayTime = driver.find_element_by_id('MTG_DAYTIME$' + str(i)).text

            days = dayTime.split()[0].encode('utf-8')  # MoWeFr

            startTime = dayTime.split()[1].encode('utf-8')  # 1:00pm

            endTime = dayTime.split()[3].encode('utf-8')  # 2:00pm

            # find room
            room = driver.find_element_by_id('MTG_ROOM$' + str(i)).text

            # find section
            instructor = driver.find_element_by_id('MTG_INSTR$' + str(i)).text

            # find section
            dateOfClass = driver.find_element_by_id('MTG_TOPIC$' + str(i)).text

            if "DIS" not in class_format or "LAB" not in class_format:
                self.ccn = classNum
                for i in range(0, len(days), 2):
                    self.days.append(days[i:i + 2])
                self.lecture_start_time = str(startTime)
                self.lecture_end_time = str(endTime)
                self.location = room
                self.instructor = instructor

            else:
                test_section = Section.Section(str(classNum))
                for i in range(0, len(days), 2):
                    test_section.days.append(days[i:i + 2])
                test_section.section_start_time = str(startTime)
                test_section.section_end_time = str(endTime)
                test_section.location = room

                if "DIS" in class_format:
                    self.add_discussion(test_section)
                elif "LAB" in class_format:
                    self.add_lab(test_section)
            return self