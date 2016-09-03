from package import Section
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        return self.subject + " " + str(self.number) + " at " + str(self.location) + ": " + \
               str(self.lecture_start_time) + "-" + str(self.lecture_end_time) + " on " + self.daysToString()

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

        try:
            moreThanFiftyClassesElement = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.XPATH, "// *[ @ id = 'DERIVED_SSE_DSP_SSR_MSG_TEXT']")))
        except:
            moreThanFiftyClassesElement = None

        if moreThanFiftyClassesElement != None:
            driver.find_element_by_xpath("//*[@id='#ICSave']").click()
            # wait_until_clickable_then_click("DERIVED_SSE_DSP_SSR_MSG_TEXT")
            driver.implicitly_wait(5)

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
            if dayTime.encode('utf-8') == "TBA":
                startTime = "TBA"
                endTime = "TBA"
            else:
                startTime = dayTime.split()[1].encode('utf-8')  # 1:00pm
                endTime = dayTime.split()[3].encode('utf-8')  # 2:00pm

            # find room
            room = driver.find_element_by_id('MTG_ROOM$' + str(i)).text

            # find section
            instructor = driver.find_element_by_id('MTG_INSTR$' + str(i)).text

            # find section
            dateOfClass = driver.find_element_by_id('MTG_TOPIC$' + str(i)).text
            if "DIS" not in class_format and "LAB" not in class_format:
                self.ccn = classNum
                if dayTime.encode('utf-8') == "TBA":
                    self.days.append("TBA")
                else:
                    for i in range(0, len(days), 2):
                        self.days.append(days[i:i + 2])
                self.lecture_start_time = str(startTime)
                self.lecture_end_time = str(endTime)
                self.location = room
                self.instructor = instructor
                self.format = class_format.encode('utf-8')

            else:
                test_section = Section.Section(str(classNum))
                for i in range(0, len(days), 2):
                    test_section.days.append(days[i:i + 2])
                test_section.section_start_time = str(startTime)
                test_section.section_end_time = str(endTime)
                test_section.location = room

                if "DIS" in class_format:
                    self.add_discussion(test_section)
                    test_section.format = "DIS"
                elif "LAB" in class_format:
                    self.add_lab(test_section)
                    test_section.format = "LAB"

        return self

    def atLeastOneDayOverlaps(self, otherClass):
        for day in otherClass.days:
            if day in self.days:
                return True
        return False

    def militaryTime(self, string_time):
        hour = int(string_time[0])
        minutes = int(string_time[2:4])
        amOrPm = string_time[len(string_time) - 2:len(string_time)]
        if amOrPm == "PM":
            hour += 12
        if minutes == 59:
            hour += 1
            return hour
        return hour + (minutes / 60.0)

    def daysToString(self):
        returnString = ""
        for i in range(len(self.days)):
            if i == len(self.days) - 1:
                returnString += self.days[i]
            else:
                returnString += self.days[i] + ", "
        return returnString