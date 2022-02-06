#!/bin/sh 
cd "$(dirname ${BASH_SOURCE[0]})/../../01_BDD_Tier/features"
behave --tags=SC-ZT-32 