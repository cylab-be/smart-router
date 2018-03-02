
class dnsquery:
    def __init__(self):
        self.ip = ""
        self.domain = ""
        self.datetime = ""

    def __init__(self, params):
        self.ip = params[0]
        self.domain = params[1]
        self.datetime = params[2]

    def __str__(self):
        return self.ip+","+self.domain+","+str(self.datetime)
