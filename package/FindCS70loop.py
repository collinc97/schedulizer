from selenium import webdriver
from package import Class
from package import Section
import re

# import pickle # from ways of safe
subjects = open("subjects.txt")
subject_list = []
for line in subjects:
    subject_list.append(re.search('>(.*)<', line).group(1))
subjects.close()

# This script opens the online schedule of classes in chrome and navigates to the possible options for cs70 fall 2016
# It should scrape all class info as stored Class class variables (to later be stored in database with fast retrieval)

# Be sure to specify path to chromedriver in webdriver.Chrone('/here/')
driver = webdriver.Chrome('/Users/bbc/chromedriver')

# #Url of classes page
# driver.get("http://schedule.berkeley.edu/")

driver.get(
    "https://bcsweb.is.berkeley.edu/psc/bcsprd_pub/EMPLOYEE/HRMS/c/COMMUNITY_ACCESS.CLASS_SEARCH.GBL?ucFrom=berkeley")
# driver.findElement(By.xpath("//*[@id=\"content\"]/table/tbody/tr[1]/td[2]/a[1]")).click();

driver.find_element_by_name('SSR_CLSRCH_WRK_SUBJECT_SRCH$0').send_keys("computer science")
driver.find_element_by_name('SSR_CLSRCH_WRK_CATALOG_NBR$1').send_keys("70")
driver.find_element_by_name('CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH').click()
driver.implicitly_wait(100)

classesText = driver.find_element_by_class_name("SSSGROUPBOX").text
parts = classesText.split(" ")
numberOfClasses = parts[0]

# run method that goes through each class and writes the important info to a .txt file
# getClassInfo(numberOfClasses)
f = open('output', 'w')
currClassNum = 0

# Initializing a class
test_class = Class.AClass("Computer Science", 70)

class_format = ""  # LEC, DIS, LAB, etc.

while currClassNum < int(numberOfClasses):
    # find class / section / dayTime / room / instructor / dateOfClass / status

    # find class
    classNum = driver.find_element_by_name('MTG_CLASS_NBR$' + str(currClassNum)).text
    f.write(classNum + ' ')

    # find section
    sectionNum = driver.find_element_by_name('MTG_CLASSNAME$' + str(currClassNum)).text
    # sectionParts = sectionText.split(' ')
    # sectionNum = sectionParts[0]
    f.write(sectionNum + ' ')
    class_format = sectionNum.split("-", 1)[1].encode('utf-8')

    # find dayTime
    dayTime = driver.find_element_by_id('MTG_DAYTIME$' + str(currClassNum)).text
    f.write(dayTime + ' ')

    # test_class.lecture_days.append(dayTime)
    days = dayTime.split()[0].encode('utf-8')  # MoWeFr

    startTime = dayTime.split()[1].encode('utf-8')  # 1:00pm

    endTime = dayTime.split()[3].encode('utf-8')  # 2:00pm

    # find room
    room = driver.find_element_by_id('MTG_ROOM$' + str(currClassNum)).text
    f.write(room + ' ')

    # find section
    instructor = driver.find_element_by_id('MTG_INSTR$' + str(currClassNum)).text
    f.write(instructor + ' ')

    # find section
    dateOfClass = driver.find_element_by_id('MTG_TOPIC$' + str(currClassNum)).text
    f.write(dateOfClass + ' ')

    if "LEC" in class_format or "REC" in class_format:
        test_class.ccn = classNum
        for i in range(0, len(days), 2):
            test_class.days.append(days[i:i+2])
        test_class.lecture_start_time = str(startTime)
        test_class.lecture_end_time = str(endTime)
        test_class.location = room
        test_class.instructor = instructor

    else:
        test_section = Section.Section(str(classNum))
        for i in range(0, len(days), 2):
            test_section.days.append(days[i:i+2])
        test_section.section_start_time = str(startTime)
        test_section.section_end_time = str(endTime)
        test_section.location = room

        if "DIS" in class_format:
            test_class.add_discussion(test_section)
        elif "LAB" in class_format:
            test_class.add_lab(test_section)

    currClassNum += 1
# closes browser
driver.close()
