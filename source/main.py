
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
from settingsHandler import settingsHandler
from icmplib import ping

class SMWinservice(win32serviceutil.ServiceFramework):
    _svc_name_ = 'ivline'
    _svc_display_name_ = 'IV Line'
    _svc_description_ = 'Ensures an active communication to the specified host.'


    @classmethod
    def parse_command_line(cls):
        win32serviceutil.HandleCommandLine(cls)
            
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.run = True
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.run = False
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, ''))
        try:
            self.main()
        except:
            servicemanager.LogErrorMsg(traceback.format_exc())
            os._exit(-1)


    def pingTest(self, hostname, maxTries):
        for i in range(maxTries):
            if (ping(hostname, 4, 1, 1).is_alive == True):
                return True
        return False

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

    def sleepWithInterrupt(self, seconds):
        if (seconds < 0): seconds = 0
        for i in range(seconds):
            if self.run == False: return True
            time.sleep(1)
        return False
        
    def main(self):
        settings = settingsHandler("C:/IVLine/", "settings.txt")
        settings.load(True)
        while self.run == True:
            self.sleepWithInterrupt(settings.pollTime)
            if self.pingTest(settings.host, settings.pingTries) == False:
                servicemanager.LogWarningMsg("Ping test failed for host \"" + settings.host + "\" Starting grace period countdown.")
                if settings.remediation == "lock": 
                    if (self.sleepWithInterrupt(settings.gracePeriod) == True):
                        servicemanager.LogInfoMsg("Service interrupted. Remediation canceled")
                    elif self.pingTest(settings.host) == True:
                        servicemanager.LogInfoMsg("Connection to \"" + settings.host + "\" has been re-established. Remediation canceled.")
                    else:
                        servicemanager.LogErrorMsg("Grace period ended and no connection to \"" + settings.host + "\" has been established. Locking machine.")
                        self.lockWindows()

                elif settings.remediation == "shutdown": 
                    self.shutdownWindows(settings.gracePeriod)

                    if (self.sleepWithInterrupt(settings.gracePeriod - 4) == True):
                        self.cancelShutdownWindows()
                        servicemanager.LogInfoMsg("Service interrupted. Remediation canceled")
                    elif self.pingTest(settings.host) == True:
                        self.cancelShutdownWindows()
                        servicemanager.LogInfoMsg("Connection to \"" + settings.host + "\" has been re-established. Remediation canceled.")
                    else:
                        servicemanager.LogErrorMsg("Grace period ended and no connection to \"" + settings.host + "\" has been established. Shutting down machine.")
                    
                    
            
                


if __name__ == '__main__':
    SMWinservice.parse_command_line()
    