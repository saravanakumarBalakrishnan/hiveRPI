import subprocess
import time


striOSAppiumConnectionString = "appium"

subprocess.call('killall node', shell=True)
subprocess.Popen(striOSAppiumConnectionString, shell=True)
time.sleep(5)
