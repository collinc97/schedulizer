class Section:

    def __init__(self, ccn):
        self.ccn = ccn
        self.days = []
        self.section_start_time = ""
        self.section_end_time = ""
        self.location = ""
        self.format = ""
        self.numEnrolled = 0
        self.size = 0

    def __str__(self):
        return str(self.section_start_time) + "-" + str(self.section_end_time) + \
               " at " + str(self.location) + " on " + self.daysToString()

    def daysToString(self):
        returnString = ""
        for i in range(len(self.days)):
            if i == len(self.days) - 1:
                returnString += self.days[i]
            else:
                returnString += self.days[i] + ", "
        return returnString