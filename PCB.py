from RCB import *
from Manager import *
class PCB:
    def __init__(self, id, parent = None, priority = 0):
        self.priority = priority ## 0,1,2
        self.id = id
        self.state = 1 ## all process when created must be ready 
        self.parent = parent

        if(parent == None):
            self.resources = list(tuple())
        else:
            self.resources = list(tuple())

        self.children = list()


    def getResources(self):
        return self.resources

    def addResource(self,rcb):
        self.resources.append(rcb)

    def removeResource(self,rcb):
        self.resources.remove(rcb)


    
                
