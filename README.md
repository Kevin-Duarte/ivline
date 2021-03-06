# IV Line
#### Developed by In Code We Speak

IV Line is a lightweight Windows service that executes an action (Lock, shutdown, etc.) on a client when a host goes down. Settings and thresholds can be modified in the settings file.

### Warnings and Disclaimers
- In Code We Speak is not responsible for damages caused by this software
- In Code We Speak is not responsible for maintenance of this software. However, feel free to reach us at support@incodewespeak.com for special requests or custom solutions.

### Installation
1. Install Python 3.9 (https://www.python.org/downloads/)
   - Ensure "Add Python 3.9 to PATH" is checked
   - Do a "Custom installation" and ensure "Install for All Users" is checked
2. Download the Github package and extract the `source` folder to `C:\Program Files\ivline\`
3. Open CMD with admin rights and run:
   - `pip install icmplib`
   - `pip install pywin32`
   - `copy "C:\Program Files\Python39\Lib\site-packages\pywin32_system32\pywintypes39.dll" "C:\Program Files\Python39\Lib\site-packages\win32"`
   - `python "C:\Program Files\ivline\source\main.py" install`  
   
### Configuration
The `settings.txt` file is stored (by default) in `C:\Program Files\ivline\settings.txt`
  - `Host`: Host to ping for heartbeat
  - `pollTime`: How often to ping the host (1 = once every second, 10 = once every 10 seconds, etc.)
  - `gracePeriod`: The amount of time for a downed host to come back online before an action is executed (seconds)
  - `action`: The action to execute once grace period has ended and host has not came back online
    - Valid Inputs: `lock`, `shutdown`
  - `pingTries`: Amount of pings to test before considering a host is down

### Starting Service
1. Open `Services.msc` and start the IV Line service
2. Go to Event Viewer > Windows Logs > Application and ensure there are no ivline errors

### Tips
- IV Line events can be monitored under Event Viewer > Windows Logs > Application
- If you want to cancel a pending action, such as a lock or shutdown, you can stop the service (Admin rights needed) via `Services.msc`
- Users with Administrator Rights can stop or modify the Service, but standard Users cannot
- Once you confirm the service is working as intended, you can set the Service Startup Type to Automatic
   - Note: Be very careful with this as you can lock-out your computer if the grace period timespan is too low
   
