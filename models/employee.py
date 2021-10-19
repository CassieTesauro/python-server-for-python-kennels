#from ch. 7

class Employee():
    def __init__(self, id, name, address, location_id = ""): #the ="" are test mode
        self.id = id
        self.name = name
        self.address = address
        self.location_id = location_id