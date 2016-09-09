class Section:

    def __init__(self, ccn):
        self.ccn = ccn
        self.days = []
        self.start_time = ""
        self.end_time = ""
        self.location = ""
        self.format = ""
        self.numEnrolled = 0
        self.size = 0

    def strWithInfo(self):
        return str(self.start_time) + "-" + str(self.end_time) + \
               " at " + str(self.location) + " on " + self.daysToString() + " " + str(self.ccn)

    def daysToString(self):
        returnString = ""
        for i in range(len(self.days)):
            if i == len(self.days) - 1:
                returnString += self.days[i]
            else:
                returnString += self.days[i] + ", "
        return returnString