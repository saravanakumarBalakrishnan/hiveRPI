#!/bin/sh 
cd $(dirname "$0")/../../01_BDD_Tier/features
behave --tags=Telegesis
