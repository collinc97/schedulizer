from selenium import webdriver, common
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from package import Class
import re

# import pickle # from ways of safe
subjects = open("subjects.txt")
subject_list = []
for line in subjects:
    subject_list.append(re.search('>(.*)<', line).group(1))
subjects.close()
pickled_data = {}

# This script opens the online schedule of classes in chrome and navigates to the possible options for cs70 fall 2016
# It should scrape all class info as stored Class class variables (to later be stored in database with fast retrieval)

# Be sure to specify path to chromedriver in webdriver.Chrone('/here/')
driver = webdriver.Chrome('/Users/bbc/chromedriver')

for i in range(5, 6): # Eventually change to range(1, len(subject_list))
    driver.get(
        "https://bcsweb.is.berkeley.edu/psc/bcsprd_pub/EMPLOYEE/HRMS/c/COMMUNITY_ACCESS.CLASS_SEARCH.GBL?ucFrom=berkeley")
    driver.find_element_by_name('SSR_CLSRCH_WRK_SUBJECT_SRCH$0').send_keys(subject_list[i])
    driver.find_element_by_name('SSR_CLSRCH_WRK_ACAD_CAREER$2').send_keys("undergraduate")
    driver.find_element_by_name('CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH').click()

    try:
        noClassElement = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//*[@id='DERIVED_CLSMSG_ERROR_TEXT']")))
    except:
        noClassElement = None

    try:
        moreThanFiftyClassesElement = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "// *[ @ id = 'DERIVED_SSE_DSP_SSR_MSG_TEXT']")))
    except:
        moreThanFiftyClassesElement = None

    if moreThanFiftyClassesElement != None:
        driver.find_element_by_xpath("//*[@id='#ICSave']").click()
        driver.implicitly_wait(2)
    if noClassElement == None:
        index = 0
        classes = []
        while True:
            try:
                class_name = driver.find_element_by_id('win0divSSR_CLSRSLT_WRK_GROUPBOX2GP$' + str(index)).text
                class_number = class_name.split()[1]
                test_class = Class.AClass(subject_list[i], class_number)
                classes.append(test_class)
                index += 1
            except common.exceptions.NoSuchElementException:
                break
                # Put data in the pickled dictionary
                # for c in classes:
                #    c.collect_data(driver)
                #    pickled_data[str(c)] = c
# Close browser
driver.close()
