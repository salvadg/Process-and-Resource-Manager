
## shell
import sys
from Manager import *
fName = "input.txt"

def handleFile(outFile):
    manager = Manager()
    with open(fName, mode = 'r') as file:
        _lines = list(line for line in (l.strip() for l in file) if line)
        for lines in _lines:
            # line = lines.rstrip('\r\n')
            line = lines.split()
            # print(line)
            if not line:
                break
            ## Case: Init 
            if line[0] == "in":
                outFile.write("\n")
                outFile.write(manager.initialize())

            ## Case: Create 
            elif line[0] == "cr":
                output = manager.create(int(line[1]))
                if output == -1:
                    outFile.write("-1 ")
                else:
                    outFile.write( output )

            ## Case: Time Out 
            elif line[0] == "to":
                outFile.write( manager.timeout() )
            
            ## Case: Request 
            elif line[0] == "rq":
                output = manager.request(int(line[1]), int(line[2]))
                if output == -1:
                    outFile.write("-1 ")
                else:
                    outFile.write(output)
            
            ## Case: Release 
            elif line[0] == "rl":
                if int(line[1]) > 3 or int(line[1]) < 0:
                    outFile.write("-1 ")
                else:
                    r = manager.rcbList[int(line[1])]
                    result = manager.release(r, int(line[2])) 
                    if result == -1:
                        outFile.write("-1 ")
                    else:
                        outFile.write( result)

            ## Case: Destroy 
            elif line[0] == "de":
                if manager.pCount <= int(line[1]):
                    outFile.write("-1 ")
                else:
                    p = manager.pcbList[int(line[1])]
                    output = manager.destroy(p)
                    if output == -1:
                        outFile.write("-1 ")
                    else:
                        outFile.write( output )

def handleInput():
    print("Test")
    manager = Manager()
    while True:
        x = raw_input().split()
        if "-1" == x[0]:
            break
    
        ## Case: Init 
        if x[0] == "in":
            print
            manager.initialize()

        ## Case: Create 
        elif x[0] == "cr":
            if manager.create(int(x[1])) == -1:
                print("-1")

        ## Case: Time Out 
        elif x[0] == "to":
            manager.timeout()     
        
        ## Case: Request 
        elif x[0] == "rq":
            if manager.request(int(x[1]), int(x[2])) == -1:
                print("-1")
        
        ## Case: Release 
        elif x[0] == "rl":
            r = manager.rcbList[int(x[1])]
            if r == -1:
                print("-1")
            else:
                manager.release(r, int(x[2]))

        ## Case: Destroy 
        elif x[0] == "de":
            p = manager.pcbList[int(x[1])]
            if p == -1:
                print("-1")
            else:
                manager.destroy(p)

def main():
    # handleInput()
    with open("output.txt", mode = 'w') as outFile:
        # pass
        handleFile(outFile)
        

if __name__ == "__main__":
    main()

