#!/bin/sh
cd $(dirname "$0")
python3 firmwareUpgrade.py
cd ../..