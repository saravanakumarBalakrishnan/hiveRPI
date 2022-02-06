#!/bin/sh
pidof -k "sh"
pkill $(ps -o pid=$(ps -ef | grep "python3.5"| awk '{print $3}')| grep -v grep| awk '{print "pid "$1}'|awk "NR>1")
pkill $(ps -o pid=$(ps -ef | grep "Python"| awk '{print $3}')| grep -v grep| awk '{print "pid "$1}')
pkill $(ps -o pid=$(ps -ef | grep "sh"| awk '{print $3}')| grep -v grep| awk '{print "pid "$1}')
pkill $(ps -o pid=$(ps -ef | grep "behave"| awk '{print $3}')| grep -v grep| awk '{print "pid "$1}')
