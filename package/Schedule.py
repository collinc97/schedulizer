import copy

class ASchedule:

    def __init__(self, classes):
        if self.existsLectureTimeConflict(classes, 0):
            return None
        self.classes = classes
    def __str__(self):
        returnString = ""
        for c in self.classes:
            returnString += str(c) + "\n"
        return returnString

    def generateSchedules(self, classes):
        lecture_only_schedule = ASchedule(classes)
        if lecture_only_schedule is not None:
            valid_schedules = [lecture_only_schedule]
            for c in self.classes:
                new_valid_schedules = []
                if hasattr(c, "discussions"):
                    if len(c.discussions) > 0:
                        for schedule in valid_schedules:
                            for dis in c.discussions:
                                if not schedule.existsTimeConflict(dis):
                                    tempSchedule = copy.deepcopy(schedule)
                                    tempSchedule.add_class(dis)
                                    new_valid_schedules.append(tempSchedule)
                        valid_schedules = new_valid_schedules
        return valid_schedules

    def existsLectureTimeConflict(self, classes, index):
        if len(classes) == 0 or len(classes) == 1:
            return False
        for i in range(index, len(classes) - 2):
            if self.atLeastOneDayOverlaps(classes[i], classes[i + 1]):
                if classes[i].lecture_start_time == classes[i + 1].lecture_start_time:
                    return True
                elif classes[i].lecture_start_time > classes[i + 1].lecture_start_time and \
                     classes[i].lecture_start_time < classes[i + 1].lecture_end_time:
                    return True
                elif classes[i + 1].lecture_start_time > classes[i].lecture_start_time and \
                     classes[i + 1].lecture_start_time < classes[i].lecture_end_time:
                    return True
        return False

    def existsTimeConflict(self, section):
        for c in self.classes:
            if self.atLeastOneDayOverlaps(c, section):
                if hasattr(c, "lecture_start_time"):
                    if c.lecture_start_time == section.section_start_time:
                        return True
                    elif c.lecture_start_time > section.section_start_time and \
                         c.lecture_start_time < section.section_end_time:
                        return True
                    elif section.section_start_time > c.lecture_start_time and \
                         section.section_start_time < c.lecture_end_time:
                        return True
                else:
                    if c.section_start_time == section.section_start_time:
                        return True
                    elif c.section_start_time > section.section_start_time and \
                         c.section_start_time < section.section_start_time:
                        return True
                    elif section.section_start_time > c.section_start_time and \
                         section.section_start_time < c.section_start_time:
                        return True
        return False

    def atLeastOneDayOverlaps(self, classOne, classTwo):
        if len([day for day in classOne.days if day in classTwo.days]) > 0:
            return True
        return False

    def add_class(self, c):
        self.classes.append(c)