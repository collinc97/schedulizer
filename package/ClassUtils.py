import urllib
import json

def findDistanceBetweenTwoClasses(classPair):
    class1 = classPair[0]
    class2 = classPair[1]
    toString = cleanLocation(class1.location)
    fromString = cleanLocation(class2.location)
    apiKey = "AIzaSyCCCF7-uLhdH9XJdJP6WMXcu4-MFXPCALo"
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?mode=walking&units=imperial" \
          "&origins=" + toString + ",Berkeley,CA" \
                                   "&destinations=" + fromString + ",Berkeley,CA&key=" \
          + apiKey
    print url
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    distance = data["rows"][0][u'elements'][0][u'duration'][u'text']
    return distance.encode('utf-8')

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
