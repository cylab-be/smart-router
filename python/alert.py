
class alert:
    def __init__(self):
        self.mac = ""
        self.hostname = ""
        self.domain_reached = ""
        self.infraction_date = ""

    def __init__(self, params):
        self.mac = params[0]
        self.hostname = params[1]
        self.domain_reached = params[2]
        self.infraction_date = params[3]

    def __str__(self):
        return self.mac+","+self.hostname+","+self.domain_reached+","+str(self.infraction_date)

    def __eq__(self, other):
        #FIXME - no nedd hostname to be equal
        if self.mac == other.mac and self.domain_reached == other.domain_reached and self.infraction_date == other.infraction_date :
            return True
        return False

    def toTuple(self):
        return "('"+ self.mac+"','"+self.hostname+"','"+self.domain_reached+"','"+str(self.infraction_date)+"')"