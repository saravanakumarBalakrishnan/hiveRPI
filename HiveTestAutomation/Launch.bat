#!/bin/sh cd -- "$(dirname "$0")
cd 01_BDD_Tier
cd features
behave --tags=SC-ZT-33
pause
