# Smart-Interviews-Score-Tracker
A tracker to see your(and your friends) progress daily. Scores from google sheets are taken with url and added to your google sheets daily and sends the status of execution.

## Getting Started
Fork the project and clone it on your desktop to start using and make necessary changes.

### Prerequisites 
Language Required
```
Python
```

Packages required 
```
smtplib
gspread
oauth2client
```

### Installing
Copy the following commands in yout terminal or command prompt 
```
pip install smtplib
pip install gspread
pip install oauth2client
```

## Changes to be made

* Give your email and password in server.login() method in send_mail function and use the mail in server.sendmail() method that you want the status to be sent. 
* In process method enter all the rows you want to track in useful_cols list. Give the location of the jason file downloaded previously in file_path vairable. In smart_interviews_url variable give the url you want to track(Make sure you have read premission). In gc.open() method give the name of your google sheet in which you want to update.
* In main method, give the names of your friends you want to track in the form of list.

Done! You are all set. Run the script and you will be getting a mail of SUCCESS. 

## Scheduling

### Mac
To Schedule this script to run at a specific time you can use launchd, which is a built-in job scheduler in mac. 
Follow these instructions

* Open terminal
* Navigate to the directory where you cloned your project
* Copy the .plist file from here to LaunchAgents folder
```
cp com.ar.scoreTracker.plist ~/Library/LaunchAgents
```
* Open .plist file in LaunchAgents folder 

```
open ~/Library/LaunchAgents/com.ar.scoreTracker.plist
```

* change the location of the script in the second string

```
<key>ProgramArguments</key>
<array>
	<string>/usr/local/bin/python3</string>
	<string>/Users/AR/Documents/Programming/Python/Pycharm/ScoreTracker/tracker.py</string>
</array>
```

* Put Hours part of the time in integer tag below the hours key, Minutes part of the time in integer tag below the integer key. 

```
<key>StartCalendarInterval</key>
<array>
    <dict>
      <key>Hour</key>
      <integer> Hours part of the time </integer>
      <key>Minute</key>
      <integer> Minutes part of the time </integer>
    </dict>
</array>
```

* Save the file and close it
* Enter the following command in terminal to load your file

```
launchctl load ~/Library/LaunchAgents/com.ar.scoreTracker.plist
```
* If you want to make any changes unload the file using following command and then make changes to it. Finally don't forget to load it again.

```
launchctl unload ~/Library/LaunchAgents/com.ar.scoreTracker.plist - unloading
```

Done! Your script will execute at the specified time daily.

Note: Your computer needs to be running for the script to be executed. If the computer is in sleep script will be executed once you wake your computer but if your computer is turned off your script will not be run. You can use pythonanywhere and kaggle to run your script on a remote server. 
