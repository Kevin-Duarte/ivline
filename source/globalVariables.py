# Global Static/Dynamic Variables 
SERVICE_NAME = 'ivline'
SERVICE_DISPLAY_NAME = 'IV Line'
SERVICE_DESCRIPTION = 'Ensures an active communication to the specified host.'
SERVICE_VERSION = '1.3'

SETTINGS_FOLDER_PATH = 'C:/Program Files/ivline/'
SETTINGS_FILENAME = "settings.txt"

# Singleton Dynamic Variables 
class DynamicGlobals:
    _instance = None
    running = False

    def getInstance():
        if DynamicGlobals._instance == None:
            DynamicGlobals()
        return DynamicGlobals._instance
    
    def __init__(self):
        if DynamicGlobals._instance != None:
            raise Exception("Error: global_variables is a singleton class. Call .getInstance().")
        else:
            #initialize here
            self.running = True
            DynamicGlobals._instance = self
            pass

# Initialization of Singleton Dynamic Variables 
dynamic_globals = DynamicGlobals.getInstance() 