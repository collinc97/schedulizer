class AClass:
    """A class for classes"""

    def __init__(self, subject, number):
        self.subject = subject
        self.number = number
        self.section = ""
        self.days = []
        self.lecture_start_time = ""
        self.lecture_end_time = ""
        self.location = ""
        self.discussions = []
        self.labs = []
        self.numEnrolled = 0
        self.size = 0

    def __str__(self):
        return self.subject + str(self.number)

    def add_discussion(self, dis):
        self.discussions.append(self, dis)

    def add_lab(self, lab):
        self.labs.append(self, lab)
