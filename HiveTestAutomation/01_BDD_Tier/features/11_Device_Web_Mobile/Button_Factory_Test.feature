# Created by kingston.samselwyn at 08/03/2017
Feature: #Factory Test for Button
  
  @SC-BU-FT-01
  Scenario Outline: SC-BU-FT-01_perform factory test and validate the output for the button.
	Given The <DeviceType> is plugged in to the port for Factory Test
	When the reset command is sent to the device and validated
	Then the test command is sent and validated
	  | TestName       |
	  | Versions       |
	  | DeviceType     |
	  | StackVersion   |
	  | EUI            |
	  | BATTERYVOLTAGE |
	  | LEDON          |
	  | LEDOFF         |
	  | RADIO11        |
	  | RADIO12        |
	  | RADIO13        |
	  | RADIO14        |
	  | RADIO15        |
	  | RADIO16        |
	  | RADIO17        |
	  | RADIO18        |
	  | RADIO19        |
	  | RADIO20        |
	  | RADIO21        |
	  | RADIO22        |
	  | RADIO23        |
	  | RADIO24        |
	  | RADIO25        |
	  | RADIO26        |
	  | RADIOSTOP      |
	  | SLEEP          |
	  | ZIGBEE         |
	  | SWITCH         |
	  | REARBUTTON     |
	
	
	Examples:
	  | DeviceType |
	  | Button01   |
	
	
  @SC-IS-FT-01
  Scenario Outline: SC-BU-FT-01_perform factory test and validate the output for the ICE Sensor.
	Given The <DeviceType> is plugged in to the port for Factory Test
	When the serial port is connected
	Then the test command is sent and validated for the sensor
	  | TestName       |
	  | Versions       |
	  | MOTIONDEVICETYPE     |
	  | StackVersion   |
	  | EUI            |
	  | TEMP            |
	  | BATTERYVOLTAGE |
	  | LUX          |
	  | LEDRON         |
	  | LEDGON         |
	  | LEDOFF         |
	  | NVM         |
	  | RADIO11        |
	  | RADIO12        |
	  | RADIO13        |
	  | RADIO14        |
	  | RADIO15        |
	  | RADIO16        |
	  | RADIO17        |
	  | RADIO18        |
	  | RADIO19        |
	  | RADIO20        |
	  | RADIO21        |
	  | RADIO22        |
	  | RADIO23        |
	  | RADIO24        |
	  | RADIO25        |
	  | RADIO26        |
	  | RADIOSTOP      |
	  | ZIGBEE11        |
	  | ZIGBEE12        |
	  | ZIGBEE13        |
	  | ZIGBEE14        |
	  | ZIGBEE15        |
	  | ZIGBEE16        |
	  | ZIGBEE17        |
	  | ZIGBEE18        |
	  | ZIGBEE19        |
	  | ZIGBEE20        |
	  | ZIGBEE21        |
	  | ZIGBEE22        |
	  | ZIGBEE23        |
	  | ZIGBEE24        |
	  | ZIGBEE25        |
	  | ZIGBEE26        |
	  | MEMORY          |
	  | PIR         |
	  | REARBUTTON     |
	
	
	Examples:
	  | DeviceType |
	  | MOT003   |
	
	
   @SC-IS-FT-02
  Scenario Outline: SC-BU-FT-02_perform factory test and validate the output for the ICE Sensor.
	Given The <DeviceType> is plugged in to the port for Factory Test
	When the serial port is connected
	Then the test command is sent and validated for the sensor
	  | TestName       |
	  | Versions       |
	  | MOTIONDEVICETYPE     |
	  | StackVersion   |
	  | EUI            |
	  | TEMP            |
	  | BATTERYVOLTAGE |
	  | LUX          |
	  | LEDRON         |
	  | LEDGON         |
	  | LEDOFF         |
	  | NVM         |
	  | RADIO11        |
	  | RADIO12        |
	  | RADIO13        |
	  | RADIO14        |
	  | RADIO15        |
	  | RADIO16        |
	  | RADIO17        |
	  | RADIO18        |
	  | RADIO19        |
	  | RADIO20        |
	  | RADIO21        |
	  | RADIO22        |
	  | RADIO23        |
	  | RADIO24        |
	  | RADIO25        |
	  | RADIO26        |
	  | RADIOSTOP      |
	  | ZIGBEE11        |
	  | ZIGBEE12        |
	  | ZIGBEE13        |
	  | ZIGBEE14        |
	  | ZIGBEE15        |
	  | ZIGBEE16        |
	  | ZIGBEE17        |
	  | ZIGBEE18        |
	  | ZIGBEE19        |
	  | ZIGBEE20        |
	  | ZIGBEE21        |
	  | ZIGBEE22        |
	  | ZIGBEE23        |
	  | ZIGBEE24        |
	  | ZIGBEE25        |
	  | ZIGBEE26        |
	  | MEMORY          |
	  | MAGNET         |
	  | REARBUTTON     |
	
	
	Examples:
	  | DeviceType |
	  | DWS003   |