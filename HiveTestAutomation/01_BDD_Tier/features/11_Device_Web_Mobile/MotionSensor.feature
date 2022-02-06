#Created on 16 July 2016
#Modified on 06 April 2017

#@authors:
#iOS        - rajeshwaran
#Android    - Sivakumar
#Web        - Selva

# ################# Variable Definitions #######################################################
# Motion Sensor	   - The name of the primary device to pass in as parameter
# NumberOf   - The no of days to go back and to see the logs in the client
################################################################################################

Feature: Validate the functionalities of Motion Sensors

  @C231903 @C130392 @SC-MS_01 @MotionSensor
  Scenario Outline: SC-MS-MC01_Validate the basic operations for Motion Sensor
    Given The <Motion Sensor> is paired with the hub
    When User navigates to the <Motion Sensor> screen in the Client
    Then Validate the current status of the <Motion Sensor> in API for for <DeviceType>
    When User navigates to the event logs in the Client
    Then Validate the motion event logs are displayed
    When User views <NumberOf> days back in the event logs in the Client
    Then Validate the motion event logs are displayed

    Examples:
      | Motion Sensor | NumberOf | DeviceType    |
      | Motion sensor |        3 | PIR00140005_1 |


  @MotionSensorStatus
  Scenario Outline: SC-SEN-STATE01_Validate the state of the motion sensor
	Given The <Motion Sensor> is paired with a Hive Hub and setup for API Validation
    When a User navigates to <Motion Sensor> screen in the Client
    Then Automatically validate the state of the <Motion Sensor>

    Examples:
      | Motion Sensor |
      | Motion Sensor |

  @MotionSensorEventlogs
  Scenario Outline: SC-SEN-EL01_Validate the brightness of Active light
	Given The <Motion Sensor> is paired with a Hive Hub and setup for API Validation
    When a User navigates to <Motion Sensor> screen in the Client
    Then Automatically validate the eventLogs of the <Motion Sensor>

    Examples:
      | Motion Sensor |
      | Motion Sensor |