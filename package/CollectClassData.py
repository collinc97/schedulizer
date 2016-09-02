from selenium import webdriver, common
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from package import Class
import re
import pickle # from ways of safe
from datetime import datetime

start_time = datetime.now()
subjects = open("subjects.txt")
subject_list = []
for line in subjects:
    subject_list.append(re.search('>(.*)<', line).group(1))
subjects.close()
pickled_data = {}
pickle_out = open("class_data.pickle", "wb")
s = set()
n = []
numClassesNotForUndergrad = 0
classes = []

# This script opens the online schedule of classes in chrome and navigates to the possible options for cs70 fall 2016
# It should scrape all class info as stored Class class variables (to later be stored in database with fast retrieval)

# Be sure to specify path to chromedriver in webdriver.Chrone('/here/')
#driver = webdriver.Chrome('/Users/bbc/chromedriver')
#driver = webdriver.PhantomJS('Users/mylifeisriley/Downloads/phantomjs-2.1.1-macosx')
driver = webdriver.Firefox()

def wait_until_clickable_then_click(id):
    # element = WebDriverWait(driver, 5, poll_frequency=.2).until(
    #     EC.element_to_be_clickable(element))
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, id))
    )
    element.click()

for i in range(0, len(subject_list)):
    driver.get(
        "https://bcsweb.is.berkeley.edu/psc/bcsprd_pub/EMPLOYEE/HRMS/c/COMMUNITY_ACCESS.CLASS_SEARCH.GBL?ucFrom=berkeley")
    driver.find_element_by_name('SSR_CLSRCH_WRK_SUBJECT_SRCH$0').send_keys(subject_list[i])
    driver.find_element_by_name('SSR_CLSRCH_WRK_ACAD_CAREER$2').send_keys("undergraduate")
    driver.find_element_by_name('CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH').click()
    #wait_until_clickable_then_click('CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH')

    try:
        noClassElement = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//*[@id='DERIVED_CLSMSG_ERROR_TEXT']")))
        print "no classes for undergrad: " + subject_list[i]
        n.append(subject_list[i])
    except:
        noClassElement = None

    try:
        moreThanFiftyClassesElement = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "// *[ @ id = 'DERIVED_SSE_DSP_SSR_MSG_TEXT']")))
    except:
        moreThanFiftyClassesElement = None

    if moreThanFiftyClassesElement != None:
        driver.find_element_by_xpath("//*[@id='#ICSave']").click()
        #wait_until_clickable_then_click("DERIVED_SSE_DSP_SSR_MSG_TEXT")
        driver.implicitly_wait(5)
    if noClassElement != None:
        numClassesNotForUndergrad += 1
    if noClassElement == None:
        index = 0
        while True:
            try:
                class_name = driver.find_element_by_id('win0divSSR_CLSRSLT_WRK_GROUPBOX2GP$' + str(index)).text
                class_number = class_name.split()[1]
                test_class = Class.AClass(subject_list[i], class_number)
                print(test_class)
                classes.append(test_class)
                s.add(test_class.subject)
                index += 1
            except common.exceptions.NoSuchElementException:
                break

    # Put data in the pickled dictionary
for c in classes:
    print("Collecting data for " + str(c))
    c.collect_data(driver)
    pickled_data[str(c)] = c

with open('class_data.pickle', 'wb') as handle:
  pickle.dump(pickled_data, handle)

print "len(s) = " + str(len(s))
print "numClassesNotForUndergrad = " + str(numClassesNotForUndergrad)
print s
print n
print str(datetime.now() - start_time)
# Close browser
driver.close()
