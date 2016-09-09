import urllib
import json
import re

def getPlaceId(place):
    apiKey = "AIzaSyBE-lTwLCv39vFnOTCON5BxT6dbueHFB7k"
    url = "https://maps.googleapis.com/maps/api/place/textsearch/xml?query=" + place + "&key=" + apiKey
    response = urllib.urlopen(url)
    data = response.read()
    print url
    placeId = re.search('<place_id>(.*)</place_id>', data).group(1)
    return placeId

def findDistanceBetweenTwoClasses(classPair):
    class1 = classPair[0]
    class2 = classPair[1]
    toString = getPlaceId(cleanLocation(class1.location))
    fromString = getPlaceId(cleanLocation(class2.location))
    apiKey = "AIzaSyCCCF7-uLhdH9XJdJP6WMXcu4-MFXPCALo"
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?mode=walking&units=imperial&origins=place_id:" + \
          toString + "&destinations=place_id:" + fromString + "&key=" + apiKey
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    distance = data["rows"][0][u'elements'][0][u'duration'][u'text']
    return int(distance.encode('utf-8').split()[0])


def cleanLocation(location):
    def hasNumbers(inputString):
        return any(char.isdigit() for char in inputString)

    returnString = ""
    location = location.split()
    for string in location:
        if hasNumbers(string.encode('utf-8')):
            returnString = returnString[:len(returnString) - 1]
            break
        returnString += string + "+"
    if returnString[len(returnString) - 1] == "+":
        returnString = returnString[:len(returnString) - 1]
    return returnString
