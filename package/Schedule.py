import copy
import ClassUtils
import functools

class ASchedule:

    def __init__(self, classes):
        if self.existsLectureTimeConflict(classes, 0):
            return None
        self.classes = classes
        self.numberOfBackToBackClasses = 0
        self.distance = float("inf")

    def getStartTime(self, aClass):
        return self.militaryTime(aClass.start_time)

    def sortClasses(self):
        self.classes = sorted(self.classes, key=self.getStartTime)
        return self.classes

    def __str__(self):
        returnString = ""
        for c in self.classes:
            returnString += c.strWithInfo() + "\n"
        return returnString

    def generateSchedules(self, classes):
        lecture_only_schedule = ASchedule(classes)
        if lecture_only_schedule is not None:
            valid_schedules = [lecture_only_schedule]
            for c in self.classes:
                new_valid_schedules = []
                if hasattr(c, "discussions") and len(c.discussions) > 0:
                    for schedule in valid_schedules:
                        for dis in c.discussions:
                            if not schedule.existsTimeConflict(dis):
                                tempSchedule = copy.deepcopy(schedule)
                                tempSchedule.add_class(dis)
                                new_valid_schedules.append(tempSchedule)
                    valid_schedules = new_valid_schedules
        return valid_schedules

    def sortSchedulesByMinDistance(self, schedules):
        def cmp(s1, s2):
            if s1.distance > s2.distance:
                return 1
            elif s2.distance > s1.distance:
                return -1
            return 0
        for s in schedules:
            s.totalDistance()
        sortedSchedules = sorted(schedules, key=functools.cmp_to_key(cmp))
        return sortedSchedules

    def existsLectureTimeConflict(self, classes, index):
        if len(classes) == 0 or len(classes) == 1:
            return False
        for i in range(index, len(classes) - 2):
            if self.atLeastOneDayOverlaps(classes[i], classes[i + 1]):
                if classes[i].start_time == classes[i + 1].start_time:
                    return True
                elif classes[i].start_time > classes[i + 1].start_time and \
                     classes[i].start_time < classes[i + 1].end_time:
                    return True
                elif classes[i + 1].start_time > classes[i].start_time and \
                     classes[i + 1].start_time < classes[i].end_time:
                    return True
        return False

    def existsTimeConflict(self, section):
        for c in self.classes:
            if self.atLeastOneDayOverlaps(c, section):
                if c.start_time == section.start_time:
                    return True
                elif c.start_time > section.start_time and \
                     c.start_time < section.end_time:
                    return True
                elif section.start_time > c.start_time and \
                     section.start_time < c.end_time:
                    return True
        return False

    def atLeastOneDayOverlaps(self, classOne, classTwo):
        if len([day for day in classOne.days if day in classTwo.days]) > 0:
            return True
        return False

    def add_class(self, c):
        self.classes.append(c)

    def militaryTime(self, string_time):
        if string_time[1] == ":":
            hour = int(string_time[0])
            minutes = int(string_time[2:4])
        else:
            hour = int(string_time[0:2])
            minutes = int(string_time[3:5])
        amOrPm = string_time[len(string_time) - 2:len(string_time)]
        if amOrPm == "PM":
            hour += 12
        if minutes == 59:
            hour += 1
            return hour
        return hour + (minutes / 60.0)

    def totalDistance(self):
        # AIzaSyA7_9tSb7YwCpul5IF_edGnqGUO6Q1Zed8 for Geocoding
        backToBacks = self.findBackToBacks()
        if len(backToBacks) > 0:
            self.distance = 0
            for classPair in backToBacks:
                distance = ClassUtils.findDistanceBetweenTwoClasses(classPair)
                self.distance += distance
        return self.distance

    def findBackToBacks(self):
        sortedClasses = self.sortClasses()
        backToBacks = []
        for i in range(len(sortedClasses) - 1):
            if self.militaryTime(sortedClasses[i].end_time) == self.militaryTime(sortedClasses[i + 1].start_time):
                daysOverlapping = self.findDaysThatOverlap(sortedClasses[i], sortedClasses[i + 1])
                if len(daysOverlapping) > 0:
                    backToBacks.append((sortedClasses[i], sortedClasses[i + 1]))
        return backToBacks

    def findDaysThatOverlap(self, class1, class2):
        overlappingDays = []
        for day in class1.days:
            if day in class2.days:
                overlappingDays.append(day)
        return overlappingDays