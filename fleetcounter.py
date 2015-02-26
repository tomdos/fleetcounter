#!/usr/bin/env  python3

import sys
       
class FleetCounter:
    def __init__(self, input):
        self.input = input
        self.empty = {'M1':0, 'M2':0, 'M3':0}
        self.full = {'M1':0, 'M2':0, 'M3':0}
        self.mostFilled = {'M1':[0,0], 'M2':[0,0], 'M3':[0,0]} # instance:[count,empty slot]


    def lineStats(self, host, instance, n, slots):
        '''Count statistics for each type - empty, full, most filled.'''

        slotsSum = sum(slots)

        if slotsSum == n:
            self.full[instance] = self.full[instance] + 1
        elif slotsSum == 0:
            self.empty[instance] = self.empty[instance] + 1
        else:
            diff = n - slotsSum
            # first entry
            if self.mostFilled[instance][0] == 0:
                self.mostFilled[instance][0] = self.mostFilled[instance][0] + 1
                self.mostFilled[instance][1] = diff
            # every other entry
            else:
                if self.mostFilled[instance][1] == diff:
                    self.mostFilled[instance][0] = self.mostFilled[instance][0] + 1
                elif self.mostFilled[instance][1] > diff:
                    self.mostFilled[instance][0] = 1
                    self.mostFilled[instance][1] = diff

    def sanityHost(self, host):
        '''
        Check and return correct form of host.
        There is no special requirements on a host formating.
        '''
        if len(host) == 0:
            sys.stderr.write("No host id.\n")
            raise RuntimeError("No host id.")

        return host

    def sanityInstance(self, instance):
        '''
        Check and return correct form of instance.
        Instance must be either {m|M}{1,2,3}
        '''
        try:
            instanceUp = instance.upper()
            self.empty[instanceUp] # Not best solution for large amount of M
        except:
            sys.stderr.write("{} '{}'\n".format(
                "Unsupported name of instance:", instance))
            raise

        return instanceUp

    def sanityN(self, n):
        '''
        Check and return correct form of N.
        N must be a number
        '''
        if n == '':
            sys.stderr.write("N is missing.\n")
            raise RuntimeError("N is missing.")        

        try:                
            nNumber = int(n)
        except:
            sys.stderr.write("N must be a number.\n")
            raise

        return nNumber

    def sanitySlots(self, n, slots):
        '''
        Check and return correct form of slots.
        Slots will be returned as a tuple.
        Number of items in the tuple must match N.
        '''
        try:
            slots = slots.split(',')
            slots = tuple(int(i) for i in slots if i == '1' or i == '0')
            if n != len(slots):
                sys.stderr.write("Wrong number of slots or value.\n")
                raise RuntimeError("Wrong number of slots or value.")
        except:
            sys.stderr.write("Slot state must be either 0 or 1.\n")
            raise

        return slots

    def processLine(self, line):
        '''Parse one line and check each item.'''
        try:
            host, instance, n, slots = line.split(',', 3) # check errors
        except:
            sys.stderr.write("{} '{}'\n".format("Can not parse line: ", line))
            raise

        # Convert(and check) an input to propper format
        try:
            host = self.sanityHost(host)
            instance = self.sanityInstance(instance)
            n = self.sanityN(n)
            slots = self.sanitySlots(n, slots)
        except:
            sys.stderr.write("Unexpected item in line: " + line + "\n")
            raise

        self.lineStats(host, instance, n, slots)


    def process(self):
        '''Process every line.'''
        try:
            for line in self.input:
                line = line.strip()
                self.processLine(line)
        except:
            sys.stderr.write("Unable to process input.\n")
            raise 

    def getStrEmpty(self):
        return "EMPTY: M1={}; M2={}; M3={};".format(self.empty['M1'],
            self.empty['M2'], self.empty['M3'])

    def getStrFull(self):
        return "FULL: M1={}; M2={}; M3={};".format(self.full['M1'],
            self.full['M2'], self.full['M3'])

    def getStrMostFilled(self):
        return "MOST FILLED: M1={},{}; M2={},{}; M3={},{};".format(
            self.mostFilled['M1'][0], self.mostFilled['M1'][1],
            self.mostFilled['M2'][0], self.mostFilled['M2'][1],
            self.mostFilled['M3'][0], self.mostFilled['M3'][1],
            )
            
            
    def printEmpty(self):
        print(self.getStrEmpty())

    def printFull(self):
        print(self.getStrFull())

    def printMostFilled(self):
        print(self.getStrMostFilled())



if __name__ == "__main__":
    INPUTFILENAME="FleetState.txt"
    OUTPUTFILENAME="Statistics.txt"
    
    try:
        fin = open(INPUTFILENAME, "r")
    except:
        sys.stderr.write("Unable to open input file '{}'\n".format(INPUTFILE))
        raise
    
    try:
        fout = open(OUTPUTFILENAME, "w")
    except: 
        sys.stderr.write("Unable to open output file '{}'\n".format(INPUTFILE))
        raise

    try:
        fc = FleetCounter(fin)
        fc.process()
        fout.write(fc.getStrEmpty()+"\n")
        fout.write(fc.getStrFull()+"\n")
        fout.write(fc.getStrMostFilled()+"\n")
            
        #fc.printEmpty()
        #fc.printFull()
        #fc.printMostFilled()
    except:
        sys.stderr.write("Could not process fleet state.\n")
        raise
    finally:
        fin.close()
        fout.close()
        
    fout.close()
    fin.close()
    
    sys.exit(0)
    
    
