import urllib
import json
import re
import pickle
import contextlib

def getPlaceId(place, place_ids):
    if place in place_ids:
        print "Already cached place: " + str(place)
        return place_ids[place]
    apiKey = "AIzaSyC1AwAjZ4oD6Cg3kmxAtiu6lOpJLiC59nw"
    url = "https://maps.googleapis.com/maps/api/place/textsearch/xml?query=" + place + "&key=" + apiKey
    with contextlib.closing(urllib.urlopen(url)) as response:
        data = response.read()
        placeId = re.search('<place_id>(.*)</place_id>', data).group(1)
        place_ids[place] = placeId
        print "Just cached: " + str(place)
    # response = urllib.urlopen(url)
    with open('place_ids.pickle', 'wb') as handle:
        pickle.dump(place_ids, handle)
    return placeId

def findDistanceBetweenTwoClasses(classPair):
    class1 = classPair[0]
    class2 = classPair[1]
    with open('place_ids.pickle', 'rb') as handle:
        place_ids = pickle.load(handle)
    toString = getPlaceId(cleanLocation(class1.location), place_ids)
    fromString = getPlaceId(cleanLocation(class2.location), place_ids)
    apiKey = "AIzaSyC1AwAjZ4oD6Cg3kmxAtiu6lOpJLiC59nw"
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
