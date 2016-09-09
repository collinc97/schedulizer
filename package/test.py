import pickle
from package import Class
from package import Schedule
from selenium import webdriver
import ClassUtils
import functools
from datetime import datetime

start_time = datetime.now()
with open('class_info.pickle', 'rb') as handle:
  class_info = pickle.load(handle)

# class_list = [class_data["History 7A"]]
class_list = [class_info["Spanish 100"], class_info["Nutritional Science &amp; Tox 10"],
              class_info["Computer Science 186"], class_info["Computer Science 188"]]
schedule = Schedule.ASchedule(class_list)
schedules = schedule.generateSchedules(schedule.classes)

print "\n Here we go \n \n"
sortedSchedules = schedules[0].sortSchedulesByMinDistance(schedules)
for s in sortedSchedules:
    print "Distance for schedule below: " + str(s.distance)
    print s
print "Generated and sorted " + str(len(schedules)) + " in "
print str(datetime.now() - start_time)
