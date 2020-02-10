

class RCB:
    def __init__(self, units):
        self.state = units
        self.waitlist = list(tuple())
        self.inventory = units

    def _checkRequest(self, k):
        if(k > self.state):
            return False
        else:
            return True

    def _checkRelease(self,totalReleased):
        sum = (totalReleased + self.state)
        if( sum > inventory):
            return False
        else:   
            self.state = sum


