class Class:
    """A class for classes"""

    def __init__(self, name):
        self.name = name
        self.lecture_start_time = ""
        self.lecture_end_time = ""
        self.discussions = []
        self.labs = []

    def add_discussion(self, dis):
        self.discussions.append(self, dis)

    def add_lab(self, lab):
        self.labs.append(self, lab)
