class ScheduleTree:
    def __init__(self, root):
        self.root = root
        self.children = []
        if len(root.discussions) != 0:
            for dis in root.discussions:
                self.children.append(dis)
        if len(root.labs) != 0:
            for lab in root.labs:
                self.children.append(lab)


