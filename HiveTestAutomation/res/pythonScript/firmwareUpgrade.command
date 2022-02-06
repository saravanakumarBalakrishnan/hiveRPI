#!/bin/sh
cd "$(dirname ${BASH_SOURCE[0]})"
python3 firmwareUpgrade.py
cd ../..