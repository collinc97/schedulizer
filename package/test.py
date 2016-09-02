import pickle
from package import Class
from selenium import webdriver

with open('class_data.pickle', 'rb') as handle:
  b = pickle.load(handle)

print b["Yiddish 101"].format
