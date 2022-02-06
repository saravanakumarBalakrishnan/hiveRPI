#Created on 10 August 2016

#@authors: 
#iOS        - Rajeshwaran
#Android    - Vinod Pasalkar
#Web        - TBD

###################Variable Definitions#######################################################
# Motion Sensor    - Name given for the Motion Sensor in the User Account
# Win/door Sensor  - Name given for the Win/door Sensor in the User Account
# Plug 			   - Name given for the Plug in the User Account
# Warm White Light - Name given for the Bulb in the User Account
# Sensor 		   - The producer of the action - Motion/Win/door sensor
# SensorState 	   - The state of the contact sensor for trigerring the action - Open / Close / Detects Motion
# TypeOf 		   - The type of notification to be set for the producer - Push / Email / Text
# Device 		   - The consumer of the Action - Plug/Active Light
# DeviceState 	   - The state of the consumer to be set - On / Off
# Duration 		   - The duration for which the Action can be set to one of these values -  Indefinitely, 30 secs,1 min, 3 mins, 5 mins, 10 mins, 15mins
##############################################################################################


Feature: Validate the various Actions available for the sensors

    @C265017 @Actions @Android_Regression @Android_SmokeTest
    Scenario Outline: SC-RB-MC01_Validate all existing Actions are removed and Action template is verified
    #Here we are removing the existing Actions to validate the action templates and begin testing from the initial state
    Given The <Motion Sensor> / <Contact Sensor> / <Plug> / <Active Light> / <Heating> are paired with the hub
    When User removes all of the existing Actions
    Then Verify if the Actions template has all available options

    Examples:
      |	Motion Sensor |	Contact Sensor	| Plug | Active Light	  | Heating |
      |	Motion sensor |	Win/door sensor	| Plug | Warm white light | Heating |
      
    @C265021 @Actions @Android_Regression @Android_SmokeTest
    Scenario Outline: SC-RB-MC02_Validate legacy Actions are set as expected
    #Verify if we are able to set the desired notification action
    Given The <Sensor> is paired with the hub
	When User sets Push notification Action for <Sensor> when <SensorState> in app
	Then the Push notification Action is displayed for <Sensor> when <SensorState> in the sensor recipe screen
    Then the Push notification Action is displayed for <Sensor> when <SensorState> in the Actions screen
	When User sets Push & Email notification Action for <Sensor> when <SensorState> in app
    Then the Push & Email notification Action is displayed for <Sensor> when <SensorState> in the Actions screen
    When User sets Text notification Action for <Sensor> when <SensorState> in app
	Then the Text notification Action is displayed for <Sensor> when <SensorState> in the Actions screen
    Examples:
      |Sensor		   | SensorState	|
      |Motion sensor   | detects motion	|
      |Win/door sensor | opened			|
      |Win/door sensor | closed			|

    @C265108 @Actions @Android_Regression @Android_SmokeTest
    Scenario Outline: SC-RB-MC03_Set Plug / Bulb Actions for the Motion sensors
    #Verify if the user can set Plug / Bulb Actions for motion sensors
    Given The <Sensor> and <Device> are paired with the hub
	When User sets <Device> to <DeviceState> for <Duration> Action for <Sensor> when <SensorState>
	Then the action is saved successfully in <Sensor> Actions screen

    Examples: 
      |	Sensor  	  | SensorState    | Device		      | DeviceState	| Duration	   |
      |	Motion sensor | detects motion | Plug		      |	On			| Indefinitely |
      |	Motion sensor | detects motion | Warm white light |	Off			| 30 secs      |
      
      
    @C265025 @Actions @Android_Regression
    Scenario Outline: SC-RB-MC04_Set Plug / Bulb Actions for the Contact sensors
    #Verify if the user can set Plug / Bulb Actions for contact sensors
    Given The <Sensor> and <Device> are paired with the hub
    When User sets <Device> to <DeviceState> for <Duration> Action for <Sensor> when <SensorState>
	Then the action is saved successfully in <Sensor> Actions screen
      
    Examples: 
      |	Sensor  		| SensorState |	Device	         | DeviceState | Duration |
      |	Win/door sensor | opened	  |	Plug	         | On		   | 15 mins  |
      |	Win/door sensor	| closed	  |	Warm white light | Off		   | 3 mins	  |

    @C265018 @Actions @Android_Regression @Android_SmokeTest
    Scenario Outline: SC-RB-MC05_Edit existing Plug / Bulb Actions for the Motion sensors
    #Verify if the user can edit the Plug / Bulb Actions for motion sensors that was set earlier
    Given The <Sensor> and <Device> are paired with the hub
	When User edits <Device> to <DeviceState> for <Duration> Action for <Sensor> when <SensorState>
	Then the action is saved successfully in <Sensor> Actions screen

    Examples: 
      |	Sensor  	  | SensorState    | Device		      | DeviceState |	Duration |
      |	Motion sensor | detects motion | Plug		      |	On		    |	1 min	 |
      |	Motion sensor | detects motion | Warm white light |	Off		    |	3 mins   |
      
    @C265112 @Actions @Android_Regression
    Scenario Outline: SC-RB-MC06_Edit Plug / Bulb Actions for the Contact sensors
    #Verify if the user can edit Plug / Bulb Actions for contact sensors that was set earlier
    Given The <Sensor> and <Device> are paired with the hub
    When User edits <Device> to <DeviceState> for <Duration> Action for <Sensor> when <SensorState>
	Then the action is saved successfully in <Sensor> Actions screen
      
    Examples: 
      |	Sensor  		| SensorState |	Device	         | DeviceState | Duration |
      |	Win/door sensor | opened	  |	Plug	         | On		   | 5 mins	  |
      |	Win/door sensor	| closed	  |	Warm white light | Off		   | 10 mins  |