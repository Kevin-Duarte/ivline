from genericpath import exists
import json
import os
from pathlib import Path

class settingsHandler:
    def __init__(self, filepath, filename):
        self.filename = filename
        self.filepath = filepath
        self.host = "8.8.8.8"
        self.pollTime = 10
        self.gracePeriod = 60
        self.remediation = "lock"
        self.pingTries = 4
    
    def modify(self, host = None, pollTime = None, gracePeriodAfterLock = None, remediation = None, pingTries = None):
        if host != None:
            self.host = host
        if pollTime != None:
            self.pollTime = pollTime
        if gracePeriodAfterLock != None:
            self.gracePeriod = gracePeriodAfterLock
        if remediation != None:
            self.remediation = remediation
        if pingTries != None:
            self.pingTries = pingTries
        self.save()

    def load(self, createIfNotPresent = False):
        if createIfNotPresent == True:
            if os.path.exists(self.filepath + self.filename) == False:
                Path(self.filepath).mkdir(parents=True)
                self.save()
        f = open(self.filepath + self.filename, 'r')
        self.__dict__ = json.loads(f.read())

    def save(self):
        f = open(self.filepath + self.filename, 'w')
        f.write(json.dumps(self.__dict__))
        f.close()