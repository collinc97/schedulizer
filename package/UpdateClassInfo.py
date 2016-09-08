import pickle
from package import Class
from package import Schedule
from selenium import webdriver

with open('class_data.pickle', 'rb') as handle:
  class_data = pickle.load(handle)

