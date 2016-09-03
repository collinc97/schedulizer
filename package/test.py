import pickle
from package import Class
from package import Schedule
from selenium import webdriver

with open('class_data.pickle', 'rb') as handle:
  class_data = pickle.load(handle)

class_list = [class_data["Computer Science 188"], class_data["Computer Science 186"], class_data["Spanish 100"],
              class_data["Nutritional Science &amp; Tox 10"]]
schedule = Schedule.ASchedule(class_list)

for s in schedule.generateSchedules(schedule.classes):
    print(s)

print len(schedule.generateSchedules(schedule.classes))
