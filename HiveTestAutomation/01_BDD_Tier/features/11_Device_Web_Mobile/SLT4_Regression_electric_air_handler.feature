Feature: Regression test automation of  SLT4 stat at a zigbee level

# These cases automate the associated SLT4 related zigbee cases
# NOTE / IMPORTANT : It is mandatory to set the SLT4 to the correct configuration before attempting to run the tests
# Wiring configurations for this test W1, Y1, Rh, G, C
# The device mode should be selected to ELECTRIC AIR HANDLER and SHOULD BE IN DUAL MODE

  @STH_US_RegressionTest @STH_REG_001
    Scenario Outline: STH_REG_001_verify if the user is able to switch to different modes
      Given the TGstick is paried with the SLT4 thermostat and the device is switched to  <temp_scale> scale
      When The stat is set to mode <device_mode>
      Then it should be switched to mode <device_mode>

      Examples: Device Modes
    |temp_scale|device_mode     |
    |FAHRENHEIT| HEAT_BOOST    |
    |FAHRENHEIT| COOL_BOOST    |
    |FAHRENHEIT| HEAT SCHEDULE |
    |FAHRENHEIT| COOL SCHEDULE |
    |FAHRENHEIT| COOL HOLD     |
    |FAHRENHEIT| DUAL HOLD     |
    |FAHRENHEIT| DUAL SCHEDULE |
    |FAHRENHEIT| OFF           |
    |CELCIUS   | HEAT_BOOST    |
    |CELCIUS   | COOL_BOOST    |
    |CELCIUS   | HEAT SCHEDULE |
    |CELCIUS   | COOL SCHEDULE |
    |CELCIUS   | COOL HOLD     |
    |CELCIUS   | DUAL HOLD     |
    |CELCIUS   | DUAL SCHEDULE |
    |CELCIUS   | OFF           |


  @STH_US_RegressionTest @STH_REG_002
      Scenario Outline: STH_REG_002_verify if the stat is able to switchg between different temperature Scale
      Given the TGstick is paried with the SLT4 thermostat and the device is switched to  <temp_scale> scale
      Then the temperature scale on the stat should be set to <temp_scale>

    Examples: Temperature scale
    |temp_scale|
    |FAHRENHEIT|
    |CELCIUS   |


  @STH_US_RegressionTest @STH_REG_003
    Scenario Outline: STH_REG_003_verify if the stat is able to be set to quick cool and heat mode
    Given the TGstick is paried with the SLT4 thermostat and the device is switched to  <temp_scale> scale
    When the device is in <device_mode> mode and the required temperature is set to <number> points <value> the ambient temperature
    Then the <device_state> should be on

    Examples: Device Valid mode transtions
    |temp_scale|value     |device_mode|number|    device_state        |
    |FAHRENHEIT|above     |HEAT_BOOST |5     |HEAT_STAGE_1 FAN_STAGE_1|
    |CELCIUS   |above     |HEAT_BOOST |5     |HEAT_STAGE_1 FAN_STAGE_1|
    |FAHRENHEIT|below     |COOL_BOOST |5     |COOL_STAGE_1 FAN_STAGE_1|
    |CELCIUS   |below     |COOL_BOOST |5     |COOL_STAGE_1 FAN_STAGE_1|


  @STH_US_RegressionTest @STH_REG_004
  Scenario Outline: STH_REG_004 verify the override values in heat boost and heat hold mode
  Given the TGstick is paried with the SLT4 thermostat and the device is switched to  <temp_scale> scale
  When the device is in <device_mode> mode and the required temperature is set to <number> points <value> the ambient temperature without protection timer validation
  When The heat temperature is overridden by <change> points
  Then The heat temperature should be changed by <change> points

  Examples: Different heat modes
  |temp_scale|value     |device_mode|number|change|
  |FAHRENHEIT|above     |HEAT_BOOST |2     |2     |
  |FAHRENHEIT|above     |HEAT HOLD  |2     |2     |
  |CELCIUS   |above     |HEAT_BOOST |2     |2     |
  |CELCIUS   |above     |HEAT HOLD  |2     |2     |


@STH_US_RegressionTest @STH_REG_005
  Scenario Outline: STH_REG_005 verify the override values in cool boost and cool hold mode
  Given the TGstick is paried with the SLT4 thermostat and the device is switched to  <temp_scale> scale
  When the device is in <device_mode> mode and the required temperature is set to <number> points <value> the ambient temperature without protection timer validation
  When The cool temperature is overridden by <change> points
  Then The cool temperature should be changed by <change> points

  Examples: Different cooling modes
  |temp_scale|value     |device_mode|number|change|
  |FAHRENHEIT|below     |COOL_BOOST |2     |2     |
  |FAHRENHEIT|below     |COOL HOLD  |2     |2     |
  |CELCIUS   |below     |COOL_BOOST |2     |2     |
  |CELCIUS   |below     |COOL HOLD  |2     |2     |


  @STH_US_RegressionTest @STH_REG_006
  Scenario Outline: STH_REG_006_verify if the protection timer functionality
    Given the TGstick is paried with the SLT4 thermostat and the device is switched to  <temp_scale> scale
    When the device is set to <device_mode> mode and the required temperature is set to <change> points <transition> the ambient temperature 2 times
      Then the <device> should be off
    #Due to sleeps that were used in the case we need a time off of like 60 seconds
      Then the protection timer should be on for 120 seconds

      Examples: Temperature scale
    |temp_scale|device_mode|change|transition|device|
    |FAHRENHEIT|COOL HOLD  |2     |below     |cooler|
    |CELCIUS   |COOL HOLD  |2     |below     |cooler|
    |CELCIUS   |HEAT HOLD  |2     |above     |heater|
    |FAHRENHEIT|HEAT HOLD  |2     |above     |heater|


    @STH_US_RegressionTest @STH_REG_007
      Scenario Outline: STH_REG_007_verify when the device is in dual mode , The temperature values can be set properly
      Given the TGstick is paried with the SLT4 thermostat and the device is switched to  <temp_scale> scale
      When the device is set to dual mode <mode> , with heating set to <heat_temp> and cooling set to <cool_temp>
      Then The heat temperature should be <heat_temp>
      Then The cool temperature should be <cool_temp>

       Examples: Different heat modes
      |temp_scale|mode     |heat_temp|cool_temp|
      |CELCIUS   |DUAL HOLD|22       |26       |


    @STH_US_RegressionTest @STH_REG_008
      Scenario Outline: STH_REG_008_verify if the device is able to toggle from Quick heat to Quick cool mode
      Given the TGstick is paried with the SLT4 thermostat and the device is switched to  <temp_scale> scale
      When the device is in HEAT_BOOST mode and the required temperature is set to 2 points above the ambient temperature
      Then the device should be in HEAT_BOOST mode
      Then The heat temperature should be changed by 0 points
      Then the device timer should be on for 26 minutes
      When the device is in COOL_BOOST mode and the required temperature is set to 2 points below the ambient temperature for 60 minutes
      Then the device should be in COOL_BOOST mode
      Then The cool temperature should be changed by 2 points
      Then the device timer should be on for 56 minutes

      Examples: Temperature scale
      |temp_scale|
      |FAHRENHEIT|
      |CELCIUS   |


    @STH_US_RegressionTest @STH_REG_009
      Scenario Outline: STH_REG_009_verify if the user is able to change the boost duration
      Given the TGstick is paried with the SLT4 thermostat and the device is switched to  <temp_scale> scale
      When the device is in <device_mode> mode and the required temperature is set to 2 points <value> the ambient temperature without protection timer validation
      Then the device timer should be on for 29 minutes
      When the device is in <device_mode> mode and the required temperature is set to 2 points <value> the ambient temperature for <duration> minutes without protection timer validation
      Then the device timer should be on for <expected_time> minutes

      Examples: Boost times
      |temp_scale|device_mode|value|duration|expected_time|
      |CELCIUS   |HEAT_BOOST |above|2       |1            |
      |FAHRENHEIT|HEAT_BOOST |above|2       |1            |
      |CELCIUS   |COOL_BOOST |below|2       |1            |
      |FAHRENHEIT|COOL_BOOST |below|2       |1            |



    @STH_US_RegressionTest @STH_REG_010
      Scenario Outline: STH_REG_010_validate the different device fan modes
      Given the TGstick is paried with the SLT4 thermostat in <temp_scale>
      When The device fan mode is set to <target_fan_mode>
      Then the device fan should be successfuly set to <target_fan_mode>

      Examples: Device fan modes
      |temp_scale|target_fan_mode|
      |CELCIUS   |AUTO           |
      |CELCIUS   |ALWAYS_ON      |
      |CELCIUS   |CIRCULATE      |
      |FAHRENHEIT|AUTO           |
      |FAHRENHEIT|ALWAYS_ON      |
      |FAHRENHEIT|CIRCULATE      |



  @STH_US_RegressionTest @STH_REG_011
    Scenario Outline: STH_REG_011_validate verify if the device is able to toggle to different modes and back to the original mode without a set point
    Given the TGstick is paried with the SLT4 thermostat in <temp_scale>
    When The stat is set to mode <from_device_mode>
    Then it should be switched to mode <from_device_mode>
    When The stat is set to mode <to_device_mode>
    Then it should be switched to mode <to_device_mode>
    When The stat is set to mode <from_device_mode>
    Then it should be switched to mode <from_device_mode>

     Examples: Device Transition modes

       |temp_scale|from_device_mode|to_device_mode|
       |FAHRENHEIT| HEAT SCHEDULE  |HEAT HOLD     |
       |FAHRENHEIT| COOL SCHEDULE  |COOL HOLD     |
       |FAHRENHEIT| DUAL SCHEDULE  |DUAL HOLD     |
       |CELCIUS   | HEAT SCHEDULE  |HEAT HOLD     |
       |CELCIUS   | COOL SCHEDULE  |COOL HOLD     |
       |CELCIUS   | DUAL SCHEDULE  |DUAL HOLD     |



  @STH_US_RegressionTest @STH_REG_012
    Scenario Outline: validate if the user is able to set the device name on the screen
    Given the TGstick is paried with the SLT4 thermostat in FAHRENHEIT
    When the device name is set to <name>
    Then the device name should be set to <name>

    Examples: Device name
    |name       |
    |test_device|
