#!/bin/sh
cd -- "$(dirname "$0")"

cd 01_BDD_Tier/features/steps/Function_Libraries
python ./verifyTGStick.py
pause