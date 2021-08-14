from globalVariables import *
from icmplib import ping
from datetime import datetime, timedelta

# Ping Test Class 
class pingTest:
    def __init__(self, host):
        self.host = host
    
    def setHost(self, host):
        self.host = host

    # Ping based on Tries
    def tries(self, maxTries):
        for i in range(maxTries):
            if (ping(self.host, 4, 1, 1).is_alive == True):
                return True
        return False
    
    # Quick ping test
    def quick(self):
        if (ping(self.host, 2, 1, 1).is_alive == True):
            return True
        return False

    # Ping based on timespan. Return Values:
    #  0 = timespan reached and no successful pings
    #  1 = successful ping returned
    #  2 = service stopped
    def timespan(self, seconds):
        if (seconds < 0): seconds = 0
        endLoopTime = datetime.now() + timedelta(seconds=seconds)
        while (datetime.now() < endLoopTime):
            if dynamic_globals.running == False:
                return 2
            if self.quick() == True:
                return 1
        return 0
