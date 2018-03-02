
class host:
    def __init__(self):
        self.mac = ""
        self.hostname = ""
        self.first_activity = ""

    def __init__(self, params):
        self.mac = params[0]
        self.hostname = params[1]
        self.first_activity = params[2]

    def __str__(self):
        return self.mac+","+self.hostname+","+str(self.first_activity)
