import pickle
from package import Class
from package import Schedule
from selenium import webdriver
import ClassUtils

with open('class_data.pickle', 'rb') as handle:
  class_data = pickle.load(handle)

# class_list = [class_data["History 7A"]]
class_list = [class_data["Spanish 100"], class_data["Computer Science 188"]]
schedule = Schedule.ASchedule(class_list)

schedules = schedule.generateSchedules(schedule.classes)
s = schedules[0]
distance = ClassUtils.findDistanceBetweenTwoClasses((s.classes[1], s.classes[2]))
print distance
print schedules[0]
