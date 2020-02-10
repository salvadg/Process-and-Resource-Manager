from PCB import *
from RCB import *

root = 1

class Manager:
    def __init__(self):
        self.readyList = {0:list(), 1:list(), 2:list()}
        # self.waitlist = tuple()
        self.pcbList = list() * 16
        self.rcbList = list() * 4
        self.pCount = 0

    def initialize(self):
        ## clearing all previous data
        self.readyList.clear()
        self.readyList = {0:list(), 1:list(), 2:list()}

        self.pcbList = list() * 16 ##del self.pcbList[:]
        self.rcbList = list() * 4 ##del self.rcbList[:]

        initPCB = PCB(0,None,0)
        self.pcbList.append(initPCB)
        self.pCount = 1

        ##insert pcb at level 0 
        self.readyList[0].append(initPCB)

        for i in range(4):
            if(i < 2):
                rcb = RCB(1)
                self.rcbList.append(rcb)
            elif(i == 2):
                rcb = RCB(2)
                self.rcbList.append(rcb)
            else:
                rcb = RCB(3)
                self.rcbList.append(rcb)
 
        return self.scheduler()
    
    def _incPcount(self):
        self.pCount +=1

    def create(self, p):
        ## check if process list full
        if self.pCount >= 16:
            return -1

        ## check if valid priority
        if p < 1 or p > 2:
            print("HERE")
            return -1

        pcb = self._getCurrentPcb() ## get running process from front of ready list
        
        newPcb = PCB(self.pCount, pcb,p)
       
        pcb.children.append(newPcb) ## add newPcb to children of current PCB

        self.pcbList.append(newPcb) ## add newPcb to list of PCBs
        self.readyList[p].append(newPcb) ## add newPcb to ready list

        self.pCount +=1

        return self.scheduler()

    def destroy(self, p):
        global root

        #  ## if destroy out of range
        # if isinstance(p, int):
        #     if p >= self.pCount:
        #         return -1
        # else:
        #     p = self.pcbList[p]
        cur = self._getCurrentPcb() ## get running process

       
        # ## check if p is child of current process
        if root == 1:
            root = 0
            if not p in cur.children :
                return -1

        for child in p.children:
            self.destroy(child)

        # p.parent.children.remove(p)

        self.pCount -= 1 ## decrement pCount 
        i = p.priority
        # p.parent = None
        # p.priority = None 

        ## removing process from ready lists
        if p in self.readyList[i]:
            self.readyList[i].remove(p)

        for r in self.rcbList:
            for pcb, k in r.waitlist:
                if p == pcb:
                    r.waitlist.remove((p,k))
                p.status = 1

        ## release all resources 
        for resource, k in p.resources:
            self._releaseHelp(resource,k,p)

        # print("process {} destroyed".format(p.id))
         
        return self.scheduler()

    def _releaseHelp(self,r, k, cur):

        for resource, unit in cur.resources:
            if r == resource:
                if k > unit:
                    return -1
                cur.resources.remove((r, unit))
                r.state = r.state + k
        
        ## check waitlist for process to be unblocked
        for p,k in r.waitlist:
            if r.state < 1:
                break
            elif r.state >= k:
                r.state = r.state - k
                p.resources.append((r,k))
                p.state = 1
                
                r.waitlist.remove((p,k))
                self.readyList[p.priority].append(p)
            else:
                break
        ## call scheduler
        return self.scheduler()







    def release(self,r, k):
        cur = self._getCurrentPcb()
        free = 0
        #Error: Releasing resource self doesn't have
        for resource in cur.resources:
            if r in resource:
                free = 1
                break
        if free == 0:
            return -1    

        for resource, unit in cur.resources:
            if r == resource:
                if k > unit:
                    return -1
                cur.resources.remove((r, unit))
                r.state = r.state + k
        
        ## check waitlist for process to be unblocked
        for p,n in r.waitlist:
            if r.state < 1:
                break
            elif r.state >= n:
                r.state = r.state - n
                p.resources.append((r,n))
                p.state = 1
                
                r.waitlist.remove((p,n))
                self.readyList[p.priority].append(p)
            else:
                break
        ## call scheduler
        return self.scheduler()
         
    def request(self, r, k):
        ## invalid resource
        if r < 0 or r > 3:
            return -1
        cur = self._getCurrentPcb()
        
        if cur.id == 0:
            return -1

        # if(r < 2 and k > r):
        #     return -1
        
        # ## requesting resource already being held by self
        for resource, x in cur.resources:
            if self.rcbList[r] == resource and (x + k) > self.rcbList[r].inventory:
                return -1
    
        ## check if RCB can fulfill request
        if self.rcbList[r].state >= k:
            self.rcbList[r].state =  self.rcbList[r].state - k
            cur.resources.append((self.rcbList[r],k))
        else:
            cur.state = 0
            self.readyList[cur.priority].remove(cur)
            self.rcbList[r].waitlist.append((cur,k))

        return self.scheduler()


    def timeout(self):
        cur = self._getCurrentPcb()
        cur.state = 0
        ## remove current PCB from front of ready list
        self.readyList[cur.priority].remove(cur)
        ## put current PCB in the back of ready list (same priority)
        self.readyList[cur.priority].append(cur)

        return self.scheduler()

    def scheduler(self):
        cur = self._getCurrentPcb()
        # print("process {} \n".format(cur.id))
        return "{} ".format(cur.id)
        # self.outFile.write("process {} currently running\n")

    def _getCurrentPcb(self):
        i = 2
        while(i >= 0):
            if self.readyList[i]:
                return self.readyList[i][0]
            i -=1

    
