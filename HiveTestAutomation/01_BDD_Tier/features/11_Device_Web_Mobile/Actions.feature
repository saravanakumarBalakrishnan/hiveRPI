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

    @ActionBasics_01 @Actions
    Scenario Outline: SC-RB-MC01_Validate all existing Actions are removed and Action template is verified
    #Here we are removing the existing Actions to validate the action templates and begin testing from the initial state
    Given The <Motion Sensor> / <Contact Sensor> / <Plug> / <Active Light> / <Heating> are paired with the hub
    When User removes all of the existing Actions
    Then Verify if the Actions template has all available options

    Examples:
      |	Motion Sensor |	Contact Sensor	| Plug | Active Light	  | Heating |
      |	Motion sensor |	Win/door sensor	| Plug | Warm white light | Heating |
      
    @ActionBasics_02 @Actions
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

    @ActionBasics_03 @Actions
    Scenario Outline: SC-RB-MC03_Set Plug / Bulb Actions for the Motion sensors
    #Verify if the user can set Plug / Bulb Actions for motion sensors
    Given The <Sensor> and <Device> are paired with the hub
	When User sets <Device> to <DeviceState> for <Duration> Action for <Sensor> when <SensorState>
	Then the action is saved successfully in <Sensor> Actions screen

    Examples: 
      |	Sensor  	  | SensorState    | Device		      | DeviceState	| Duration	   |
      |	Motion sensor | detects motion | Plug		      |	On			| Indefinitely |
      |	Motion sensor | detects motion | Warm white light |	Off			| 30 secs      |
      
      
    @ActionBasics_04 @Actions
    Scenario Outline: SC-RB-MC04_Set Plug / Bulb Actions for the Contact sensors
    #Verify if the user can set Plug / Bulb Actions for contact sensors
    Given The <Sensor> and <Device> are paired with the hub
    When User sets <Device> to <DeviceState> for <Duration> Action for <Sensor> when <SensorState>
	Then the action is saved successfully in <Sensor> Actions screen
      
    Examples: 
      |	Sensor  		| SensorState |	Device	         | DeviceState | Duration |
      |	Win/door sensor | opened	  |	Plug	         | On		   | 15 mins  |
      |	Win/door sensor	| closed	  |	Warm white light | Off		   | 3 mins	  |

    @ActionBasics_05 @Actions
    Scenario Outline: SC-RB-MC05_Edit existing Plug / Bulb Actions for the Motion sensors
    #Verify if the user can edit the Plug / Bulb Actions for motion sensors that was set earlier
    Given The <Sensor> and <Device> are paired with the hub
	When User edits <Device> to <DeviceState> for <Duration> Action for <Sensor> when <SensorState>
	Then the action is saved successfully in <Sensor> Actions screen

    Examples: 
      |	Sensor  	  | SensorState    | Device		      | DeviceState |	Duration |
      |	Motion sensor | detects motion | Plug		      |	On		    |	1 min	 |
      |	Motion sensor | detects motion | Warm white light |	Off		    |	3 mins   |
      
    @ActionBasics_06 @Actions
    Scenario Outline: SC-RB-MC06_Edit Plug / Bulb Actions for the Contact sensors
    #Verify if the user can edit Plug / Bulb Actions for contact sensors that was set earlier
    Given The <Sensor> and <Device> are paired with the hub
    When User edits <Device> to <DeviceState> for <Duration> Action for <Sensor> when <SensorState>
	Then the action is saved successfully in <Sensor> Actions screen
      
    Examples: 
      |	Sensor  		| SensorState |	Device	         | DeviceState | Duration |
      |	Win/door sensor | opened	  |	Plug	         | On		   | 5 mins	  |
      |	Win/door sensor	| closed	  |	Warm white light | Off		   | 10 mins  |

    @ActionBasics_07 @Actions
    Scenario Outline: SC-RB-MC07_Calculate number of templates available under particular category
    #Calculate number of templates available under particular category
    #Here the category means WelcomeHome for UK as well as US , comfort, reassurance , efficiancy , devices like plugs , lights , etc.. and  canvas (means build your own)
    Given The <Sensor> and <Device> are paired with the hub
	Then the action templates for WelcomeHomeUK are
    Then the action templates for WelcomeHomeUS are
    Then the action templates for comfort are
    Then the action templates for reassurance are
    Then the action templates for efficiency are
    Then the action templates for temperature are
    Then the action templates for plug are
    Then the action templates for light are
    Then the action templates for motion-sensor are
    Then the action templates for contact-sensor are
    Then the action templates for hotwater are
    Then the action templates for canvas are
    Then the action templates for heating are
    Then the action templates for humidity are
    Then the action templates for light-dark are
    Then the action templates for nathermostat are
    Then the action templates for notification are
    Then the action templates for quick-action are
    Then the action templates for schedule are
    Then the action templates for sense are
    Then the action templates for sunrise-sunset  are
    Then the action templates for HomeCheck  are
    Then the free action templates are
    Then the paid action templates are

    Examples:
      |	Sensor  		| Device |
      |	Win/door sensor |  Plug  |


   @ActionBasics_08 @Actions
      Scenario Outline: SC-RB-MC08_Calculate number of free and paid templates
      #Calculate number of free and paid templates
      #Here the 'free' means the one which does not need an entitlement and 'paid' means the one's which needs an entitlement
      Given The <Sensor> and <Device> are paired with the hub
      Then the welcome home action templates are
      Then the free action templates are
      Then the paid action templates are
      Then the build your own action templates are

    Examples:
      |	Sensor  		|	Device |
      |	Win/door sensor |    Plug  |

   @ActionBasics_09 @Actions
    Scenario Outline: SC-RB-MC09_Verify all the Actions templates available under particular category.
    #Here we are navigating to specific category of action templates from discovery and verifying the templates present under it from backend as well as app UI
    # Languages can be UK_English, US_English, Canadian_English, US_Spanish, Canadian_French, Italian, Irish
    # Provide "subscribed" if need to add hive live subscription and provide "not subscribed" if hive live needs to be removed ( Same applies for LEAK ALERT PLAN )
    Given The device and user language is set to UK_English
    And The user is subscribed to HIVE LIVE
    When User taps on Welcome Home on Discover Actions
    Then The templates for Welcome Home are shown
    When User taps on Comfort on Discover Actions
    Then The templates for Comfort are shown
    When User taps on Reassurance on Discover Actions
    Then The templates for Reassurance are shown
    When User taps on Efficiency on Discover Actions
    Then The templates for Efficiency are shown
    When User taps on Thermostat on Discover Actions
    Then The templates for Thermostat are shown
    When User taps on Plugs on Discover Actions
    Then The templates for Plugs are shown
    When User taps on Lights on Discover Actions
    Then The templates for Lights are shown
    When User taps on Motion Sensor on Discover Actions
    Then The templates for Motion Sensor are shown
    When User taps on Win/Door Sensor on Discover Actions
    Then The templates for Win/Door Sensor are shown
    When User taps on Hot Water on Discover Actions
    Then The templates for Hot Water are shown
    When User taps on All actions on Discover Actions
    Then The templates for All actions are shown
    When User taps on Build Your Own on Discover Actions
    Then The templates for Build Your Own are shown

     Examples:
      |	Motion Sensor |	Contact Sensor	| Plug | Active Light	  | Heating |
      |	Motion sensor |	Win/door sensor	| Plug | Warm white light | Heating |
