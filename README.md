# IV Line
#### Developed by In Code We Speak

IV Line is a service that executes an action (Lock, shutdown, etc.) on the host operating system when ICMP pings fail. Settings and thresholds can be modified at the settings file.

### Warning and Disclaimers
- In Code We Speak is not responsible for damages caused by this software
- In Code We Speak is not responsible for maintenance on this software. However, feel free to reach us at support@incodewespeak.com for special requests or custom solutions.

### Installation
1. Install Python 3.9 or higher (https://www.python.org/downloads/)
   
   Note: Ensure "Add Python 3.9 to PATH" is checked during install
2. Run command `pip install icmplib`
3. Download the Github package and extract the source folder to `C:\Program Files\ivline\`
4. Open CMD with Admin Rights and run command `python "C:\Program Files\ivline\source\main.py" install`
5. Open `Services.msc` and start the IV Line service   
   
### Configuration
The `settings.txt` file is stored (by default) in `C:\Program Files\ivline\settings.txt`
  - `Host`: Host to ping for heartbeat
  - `pollTime`: How often to ping the host (1 = once every second, 10 = once every 10 seconds, etc.)
  - `gracePeriod`: The amount of time for a downed host to come back online before an action is executed
  - `action`: The action to execute once grace period has ended and host has not came back online
    - Valid Inputs: `lock`, `shutdown`
  - `pingTries`: Amount of pings to test before considering a host is down

### Starting Service
1. Open `Services.msc` and start the IV Line service
2. If needed, you can set the Startup Type to Automatic once you confirm it is working as intended
3. Monitor the events under Event Viewer > Windows Logs > Application
