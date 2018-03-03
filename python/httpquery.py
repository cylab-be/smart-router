
class httpquery:
    def __init__(self):
        self.mac_iot = ""
        self.domain = ""
        self.datetime = ""

    def __init__(self, params):
        self.mac_iot = params[0]
        self.domain = params[1]
        self.datetime = params[2]

    def __str__(self):
        return self.mac_iot+","+self.domain+","+str(self.datetime)

    def toSlack(self):
        return self.mac_iot+" -> "+self.domain+" @ "+str(self.datetime)
