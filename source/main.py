# Developed by In Code We Speak
# IV Line:
# Executes an action (Lock, shutdown, etc.) to host operating system
# when ICMP pings fail. Settings and thresholds can be modified at the
# settings file of the service.

import socket
import win32serviceutil
import servicemanager
import win32event
import win32service
import win32con
import win32process
import win32ts
import win32profile
import os
import traceback
import time
from globalVariables import *
from datetime import datetime, timedelta
from settingsHandler import settingsHandler
from pingTest import pingTest


class SMWinservice(win32serviceutil.ServiceFramework):
    _svc_name_ = SERVICE_NAME
    _svc_display_name_ = SERVICE_DISPLAY_NAME
    _svc_description_ = SERVICE_DESCRIPTION
    ping = pingTest('')
    
    @classmethod
    def parse_command_line(cls):
        win32serviceutil.HandleCommandLine(cls)
    
    # Initialization 
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.run = True
        socket.setdefaulttimeout(60)

    # Service Stop
    def SvcStop(self):
        servicemanager.LogInfoMsg(str(SERVICE_NAME) + " is ending.")
        dynamic_globals.running = False
        self.run = False
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    # Service Run
    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, ''))
        servicemanager.LogInfoMsg(SERVICE_DISPLAY_NAME + " " + SERVICE_VERSION + " - Developed by In Code We Speak")
        try:
            self.main()
        except:
            servicemanager.LogErrorMsg(traceback.format_exc())
            os._exit(-1)

    # Run commands within session context
    def runCommandInSession(self, command):
        console_session_id = win32ts.WTSGetActiveConsoleSessionId()
        console_user_token = win32ts.WTSQueryUserToken(console_session_id)
        startup = win32process.STARTUPINFO()
        priority = win32con.NORMAL_PRIORITY_CLASS
        environment = win32profile.CreateEnvironmentBlock(console_user_token, False)
        handle, thread_id ,pid, tid = win32process.CreateProcessAsUser(console_user_token, None, command, None, None, True, priority, environment, None, startup)

    def cancelShutdownWindows(self):
        self.runCommandInSession("shutdown.exe -a")

    def shutdownWindows(self, seconds):
        self.runCommandInSession("shutdown.exe /s /t " + str(seconds))

    def lockWindows(self):
        self.runCommandInSession("rundll32.exe user32.dll,LockWorkStation")

    # Sleep with service-running interrupt 
    def sleepWithInterrupt(self, seconds):
        if (seconds < 0): seconds = 0
        for i in range(seconds):
            if dynamic_globals.running == False: return True
            time.sleep(1)
        return False

    # Main loop
    def main(self):
        settings = settingsHandler()
        settings.load(True)
        self.ping.setHost(settings.host)
        while dynamic_globals.running == True:
            self.sleepWithInterrupt(settings.pollTime)
            # Check for ping test fails
            if self.ping.tries(settings.pingTries) == False:
                servicemanager.LogWarningMsg("Ping test failed for host \"" + settings.host + "\" Starting grace period countdown of " + str(settings.gracePeriod))

                # Lock Option
                if settings.action == "lock": 
                    result = self.ping.timespan(settings.gracePeriod)
                    if (result == 2):
                        servicemanager.LogInfoMsg("Service interrupted. Lock canceled")
                    elif (result == 1):
                        servicemanager.LogInfoMsg("Connection to \"" + settings.host + "\" has been re-established. Lock canceled.")
                    else:
                        servicemanager.LogErrorMsg("Grace period ended and no connection to \"" + settings.host + "\" has been established. Locking machine.")
                        self.lockWindows()

                # Shutdown Option
                elif settings.action == "shutdown": 
                    self.shutdownWindows(settings.gracePeriod)
                    result = self.ping.timespan(settings.gracePeriod)
                    if (result == 2):
                        self.cancelShutdownWindows()
                        servicemanager.LogInfoMsg("Service interrupted. Shutdown canceled")
                    elif (result == 1):
                        self.cancelShutdownWindows()
                        servicemanager.LogInfoMsg("Connection to \"" + settings.host + "\" has been re-established. Shutdown canceled.")
                    else:
                        servicemanager.LogErrorMsg("Grace period ended and no connection to \"" + settings.host + "\" has been established. Shutting down machine.")
                    
                    
if __name__ == '__main__':
    SMWinservice.parse_command_line()
    