class Stations(object):
    def __init__(self, name, critical = False):

        self.name = name
        self.critical = critical
        self.neighbors = []
