from package import ScheduleTree

class Schedule:

    def __init__(self, *classes):
        self.classes = classes

    def generateSchedule(self, classes):
        if self.existsTimeConflict(classes):
            return None
        else:
            for c in classes:
                tree = ScheduleTree(c)

            return "Schedule"

    def existsTimeConflict(self, classes):
        if len(classes) == 0 or len(classes) == 1:
            return False
        for i in range(len(classes) - 2):
            if classes[i].start_time == classes[i + 1].start_time:
                return True
            elif classes[i].start_time > classes[i + 1].start_time and \
                 classes[i].start_time < classes[i + 1].start_time:
                return True
            elif classes[i + 1].start_time > classes[i].start_time and \
                 classes[i + 1].start_time < classes[i].start_time:
                return True
        return False