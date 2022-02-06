#!/usr/bin/env bash
ps -ef | grep "python3.5"| awk '{print $3}'| grep -v grep|awk "NR>1" | xargs kill -9
ps -ef | grep "Python"| awk '{print $3}'| grep -v grep| xargs kill -9
ps -ef | grep "behave"| awk '{print $3}'| grep -v grep| xargs kill -9
ps -ef | grep "sh"| awk '{print $3}'| grep -v grep| xargs kill -9
