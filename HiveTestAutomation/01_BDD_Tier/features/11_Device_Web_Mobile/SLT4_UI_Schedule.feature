# Created by anand.ramakrishnan at 29/1/2018
Feature: Regression cases for SLT4 stat to validate schedule from UI


  @STH_US_RegressionTest_UI1 @STH_SCH_UI_REG_001
  Scenario Outline: STH_SCH_UI_REG_001_Set the given custom 'six' event schedule for the whole week and reset the value in celcius scale
    Given the TGstick is paried with the SLT4 thermostat and the device is switched to  <temp_scale> scale for UI based validation
    When the stat is switched to the mode <inital_mode> in UI
    Then The device should be successfully switched to <inital_mode> in UI
    When The Below <reset_mode> is set in the UI
      | Day | Event1     | Event2     | Event3     | Event4     | Event5     | Event6     |
      | WED | 06:30,23.0 | 08:15,25.0 | 10:30,17.0 | 12:00,20.0 | 13:30,26.5 | 15:00,23.0 |
    Then The device should be successfully switched to <reset_mode> in UI
    Examples: Different schedule modes
    |temp_scale|inital_mode    |reset_mode     |
    |CELCIUS   |HEAT SCHEDULE  |COOL SCHEDULE  |
    |CELCIUS   |COOL SCHEDULE  |HEAT SCHEDULE  |


  @STH_US_RegressionTest_UI1 @STH_SCH_UI_REG_002
  Scenario Outline: STH_SCH_UI_REG_002_Set the given custom 'six' event schedule for the whole week and reset the value in fahrenheit scale
    Given the TGstick is paried with the SLT4 thermostat and the device is switched to  <temp_scale> scale for UI based validation
    When the stat is switched to the mode <inital_mode> in UI
    Then The device should be successfully switched to <inital_mode> in UI
    When The Below <reset_mode> is set in the UI
      | Day   | Event1     | Event2     | Event3     | Event4     | Event5     | Event6     |
      | WED   | 06:30,73.0 | 08:30,80.0 | 11:30,69.0 | 13:00,82.0 | 15:30,73.0 | 17:45,79.0 |
    Then The device should be successfully switched to <reset_mode> in UI
    Examples: Different schedule modes
    |temp_scale   |inital_mode    |reset_mode     |
    |FAHRENHEIT   |HEAT SCHEDULE  |COOL SCHEDULE  |
    |FAHRENHEIT   |COOL SCHEDULE  |HEAT SCHEDULE  |


  @STH_US_RegressionTest_UI @STH_SCH_UI_REG_003
  Scenario Outline: STH_SCH_UI_REG_003 verify the given heat schedule is override by a values in fahrenheit scale
    Given the TGstick is paried with the SLT4 thermostat and the device is switched to  FAHRENHEIT scale for UI based validation
    When The Below <device_mode> is set in the UI
      | Day   | Event1     | Event2     | Event3     | Event4     | Event5     | Event6     |
      | Today | 06:30,70.0 | 08:30,80.0 | 11:30,69.0 | 13:00,82.0 | 15:30,70.0 | 17:15,75.0 |
    Then The device should be successfully switched to <device_mode> in UI
    When The stat heat temperature is overridden by <change> degrees via UI
    Then The heat temperature should be overridden in UI by <change> points
    Examples: Different schedule modes
    |device_mode    |change|
    |HEAT SCHEDULE  |2     |
    |HEAT SCHEDULE  |3     |

  @STH_US_RegressionTest_UI @STH_SCH_UI_REG_004
  Scenario Outline: STH_SCH_UI_REG_004 verify the given cool schedule is override by a values in fahrenheit scale
    Given the TGstick is paried with the SLT4 thermostat and the device is switched to  FAHRENHEIT scale for UI based validation
    When The Below <device_mode> is set in the UI
      | Day   | Event1     | Event2     | Event3     | Event4     | Event5     | Event6     |
      | Today | 06:30,70.0 | 08:30,80.0 | 11:30,69.0 | 13:00,82.0 | 15:30,70.0 | 17:15,75.0 |
    Then The device should be successfully switched to <device_mode> in UI
    When The stat cool temperature is overridden by <change> degrees via UI
    Then The cool temperature should be overridden in UI by <change> points
    Examples: Different schedule modes
    |device_mode    |change|
    |COOL SCHEDULE  |4     |
    |COOL SCHEDULE  |5     |


  @STH_US_RegressionTest_UI @STH_SCH_UI_REG_005
  Scenario Outline: STH_SCH_UI_REG_005 verify the given heat schedule is override by a values in celcius scale
    Given the TGstick is paried with the SLT4 thermostat and the device is switched to  CELCIUS scale for UI based validation
    When The Below <device_mode> is set in the UI
      | Day   | Event1     | Event2     | Event3     | Event4     | Event5     | Event6     |
      | WED   | 06:30,23.0 | 08:15,25.0 | 10:30,17.0 | 12:00,20.0 | 13:30,26.5 | 15:00,23.0 |
    Then The device should be successfully switched to <device_mode> in UI
    When The stat heat temperature is overridden by <change> degrees via UI
    Then The heat temperature should be overridden in UI by <change> points
    Examples: Different schedule modes
    |device_mode    |change|
    |HEAT SCHEDULE  |2     |
    |HEAT SCHEDULE  |3     |

  @STH_US_RegressionTest_UI @STH_SCH_UI_REG_006
  Scenario Outline: STH_SCH_UI_REG_006 verify the given cool schedule is override by a values in celcius scale
    Given the TGstick is paried with the SLT4 thermostat and the device is switched to  CELCIUS scale for UI based validation
    When The Below <device_mode> is set in the UI
      | Day   | Event1     | Event2     | Event3     | Event4     | Event5     | Event6     |
      | WED   | 06:30,23.0 | 08:15,25.0 | 10:30,17.0 | 12:00,20.0 | 13:30,26.5 | 15:00,23.0 |
    Then The device should be successfully switched to <device_mode> in UI
    When The stat cool temperature is overridden by <change> degrees via UI
    Then The cool temperature should be overridden in UI by <change> points
    Examples: Different schedule modes
    |device_mode    |change|
    |COOL SCHEDULE  |2     |
    |COOL SCHEDULE  |3     |




  @STH_US_RegressionTest_UI @STH_SCH_UI_REG_007
    Scenario Outline: STH_SCH_UI_REG_007_Set the given custom 'six' event schedule for today & powercycled in fahrenheit scale from UI
    Given the TGstick is paried with the SLT4 thermostat and the device is switched to  FAHRENHEIT scale for UI based validation
    When The Below <device_mode> is set in the UI
      | Day   | Event1     | Event2     | Event3     | Event4     | Event5     | Event6     |
      | Today | 06:30,80.0 | 10:30,80.0 | 13:30,69.0 | 16:00,82.0 | 19:30,88.5 | 20:45,62.0 |
    Then The device should be successfully switched to <device_mode> in UI
    When The device is rebooted
    Then The device should be successfully switched to <device_mode> in UI
    Examples: Different schedule modes
    |device_mode    |
    |HEAT SCHEDULE  |
    |COOL SCHEDULE  |

  @STH_US_RegressionTest_UI @STH_SCH_UI_REG_008
    Scenario Outline: STH_SCH_UI_REG_008_Set the given custom 'six' event schedule for today & powercycled in celcius scale from UI
    Given the TGstick is paried with the SLT4 thermostat and the device is switched to  CELCIUS scale for UI based validation
    When The Below <device_mode> is set in the UI
      | Day | Event1     | Event2     | Event3     | Event4     | Event5     | Event6     |
      | TUE | 06:30,23.0 | 08:15,25.0 | 10:30,17.0 | 12:00,20.0 | 13:30,26.5 | 15:00,23.0 |
    Then The device should be successfully switched to <device_mode> in UI
    When The device is rebooted
    Then The device should be successfully switched to <device_mode> in UI
    Examples: Different schedule modes
    |device_mode    |
    |HEAT SCHEDULE  |
    |COOL SCHEDULE  |
