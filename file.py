class File:
    def __init__(self, name):
        self.name = name
        self.data = ""
        self.saved = False
        self.path = ""

    def set_path(self, name, path):
        self.saved = True
        self.name = name
        self.path = path

    def get_path(self):
        if self.saved:
            return self.path
        else:
            return None
