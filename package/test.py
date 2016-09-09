import pickle
from package import Class
from package import Schedule
from selenium import webdriver
import ClassUtils
import functools

with open('class_info.pickle', 'rb') as handle:
  class_data = pickle.load(handle)

# class_list = [class_data["History 7A"]]
class_list = [class_data["Spanish 100"], class_data["Computer Science 188"], class_data["Computer Science 186"]]
schedule = Schedule.ASchedule(class_list)

schedules = schedule.generateSchedules(schedule.classes)

print "\n Here we go \n \n"
sortedSchedules = schedules[0].sortSchedulesByMinDistance(schedules)
for s in sortedSchedules:
    print "Distance for schedule below: " + str(s.distance)
    print s
