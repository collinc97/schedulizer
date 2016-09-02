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
        return self.section
