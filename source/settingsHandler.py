from genericpath import exists
import json
import os
from pathlib import Path
from globalVariables import *

# Settings class
class settingsHandler:
    # Default values
    # Values if settings file not present
    def __init__(self):
        self.host = "8.8.8.8"
        self.pollTime = 10
        self.gracePeriod = 60
        self.action = "lock"
        self.pingTries = 4
    
    # Update settings
    def modify(self, host = None, pollTime = None, gracePeriodAfterLock = None, remediation = None, pingTries = None):
        if host != None:
            self.host = host
        if pollTime != None:
            self.pollTime = pollTime
        if gracePeriodAfterLock != None:
            self.gracePeriod = gracePeriodAfterLock
        if remediation != None:
            self.action = remediation
        if pingTries != None:
            self.pingTries = pingTries
        self.save()

    # Load settings
    def load(self, createIfNotPresent = False):
        if createIfNotPresent == True:
            if os.path.exists(SETTINGS_FOLDER_PATH + SETTINGS_FILENAME) == False:
                if os.path.exists(SETTINGS_FOLDER_PATH) == True:
                    self.save()
                else:
                    Path(SETTINGS_FOLDER_PATH).mkdir(parents=True)
                    self.save()
        f = open(SETTINGS_FOLDER_PATH + SETTINGS_FILENAME, 'r')
        self.__dict__ = json.loads(f.read())

    # Save settings
    def save(self):
        f = open(SETTINGS_FOLDER_PATH + SETTINGS_FILENAME, 'w')
        f.write(json.dumps(self.__dict__))
        f.close()