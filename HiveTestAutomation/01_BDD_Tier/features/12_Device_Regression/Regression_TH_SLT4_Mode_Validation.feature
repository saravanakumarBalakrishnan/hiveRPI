# Created by bharath.gopalan at 02/08/2017
Feature: To validate the end functionality of the SLT4 stat at a zigbee level (HEAT HOLD and COOL HOLD)
  # These cases automate the associated SLT4 related zigbee cases
  #It is mandatory to set the SLT4 to the correct configuration before attempting to run the tests


  @STH_US_RegressionTest @STH_REG_001
  Scenario Outline: STH_REG_001_verify if the device turns on the heater when there is a heating demand in heat hold mode
    Given the TGstick is paried with the SLT4 thermostat in <temp_scale>
    When the device is in HEAT HOLD mode and the required temperature is set to 5 points above the ambient temperature
    Then the HEAT_STAGE_1 FAN_STAGE_1 should be on

    Examples: Temperature scale
    |temp_scale|
    |FAHRENHEIT|
    |   CELCIUS|


    @STH_US_RegressionTest @STH_REG_002
  Scenario Outline: STH_REG_002_verify if the device turns off the heater when there is no heating demand in heat hold mode
    Given the TGstick is paried with the SLT4 thermostat in <temp_scale>
    When the device is in HEAT HOLD mode and the required temperature is set to 5 points below the ambient temperature
    Then the heater should be off

    Examples: Temperature scale
    |temp_scale|
    |FAHRENHEIT|
    |   CELCIUS|


    @STH_US_RegressionTest @STH_REG_003
  Scenario Outline: STH_REG_003_verify if the protection timer starts for 180 seconds when the heater is turned on and off repeatedly in heat hold mode
    Given the TGstick is paried with the SLT4 thermostat in <temp_scale>
    When the device is set to HEAT HOLD mode and the required temperature is set to 5 points below the ambient temperature 2 times
      Then the heater should be off
      Then the protection timer should be on for 165 seconds

      Examples: Temperature scale
    |temp_scale|
    |FAHRENHEIT|
    |   CELCIUS|

    @STH_US_RegressionTest @STH_REG_004
    Scenario Outline:STH_REG_004_verify if the device turns heater on for the specified duration in quick heat mode when there is a heating demand
      Given the TGstick is paried with the SLT4 thermostat in <temp_scale>
      When the device is in HEAT_BOOST mode and the required temperature is set to 5 points above the ambient temperature for 3 minutes
      Then the HEAT_STAGE_1 FAN_STAGE_1 should be on
      Then the device timer should be on for 2 minutes

      Examples: Temperature scale
    |temp_scale|
    |FAHRENHEIT|
    |   CELCIUS|

       @STH_US_RegressionTest @STH_REG_005
    Scenario Outline:STH_REG_005_verify if the heater does not turn on on quik heat mode, however timer runs, when there is no hearing demand
      Given the TGstick is paried with the SLT4 thermostat in <temp_scale>
      When the device is in HEAT_BOOST mode and the required temperature is set to 5 points below the ambient temperature for 3 minutes
      Then the heater should be off
         #An approximation done here
      Then the device timer should be on for 2 minutes

      Examples: Temperature scale
    |temp_scale|
    |FAHRENHEIT|
    |   CELCIUS|


  @STH_US_RegressionTest @STH_REG_006
  Scenario Outline: STH_REG_006_verify if the user is able to cancel quick heat mode and the stat returns to the previous state
     Given the TGstick is paried with the SLT4 thermostat in <temp_scale>
    When the device is in HEAT_BOOST mode and the required temperature is set to 5 points below the ambient temperature for 30 minutes
    When the user cancels quick mode
    Then the QUICK_HEAT mode should be cancelled
    Then the stat should return to the previous state

      Examples: Temperature scale
    |temp_scale|
    |FAHRENHEIT|
    |   CELCIUS|

    @STH_US_RegressionTest @STH_REG_007
    Scenario Outline: STH_REG_007_verify if the user is able to switch modes
      Given the TGstick is paried with the SLT4 thermostat in <temp_scale>
      When the device switches from HEAT HOLD to <final_mode>
      Then the change to <final_mode> should be successful

      Examples: Temperature scale
    |temp_scale|final_mode     |
    |FAHRENHEIT| HEAT_BOOST    |
    |FAHRENHEIT| COOL_BOOST    |
    |FAHRENHEIT| HEAT SCHEDULE |
    |FAHRENHEIT| COOL SCHEDULE |
    |FAHRENHEIT| COOL HOLD     |
    |FAHRENHEIT| DUAL HOLD     |
    |FAHRENHEIT| DUAL SCHEDULE |
    |CELCIUS   | HEAT_BOOST    |
    |CELCIUS   | COOL_BOOST    |
    |CELCIUS   | HEAT SCHEDULE |
    |CELCIUS   | COOL SCHEDULE |
    |CELCIUS   | COOL HOLD     |
    |CELCIUS   | DUAL HOLD     |
    |CELCIUS   | DUAL SCHEDULE |


  @STH_US_RegressionTest @STH_REG_008
  Scenario Outline: STH_REG_008_verify if the device turns on the cooler when there is a cooling demand in cool hold mode
    Given the TGstick is paried with the SLT4 thermostat in <temp_scale>
    When the device is in COOL HOLD mode and the required temperature is set to 5 points below the ambient temperature
    Then the COOL_STAGE_1 FAN_STAGE_1 should be on

    Examples: Temperature scale
    |temp_scale|
    |FAHRENHEIT|
    |   CELCIUS|

  @STH_US_RegressionTest @STH_REG_009
  Scenario Outline: STH_REG_009_verify if the device turns off the cooler when there is no cooling demand in heat hold mode
    Given the TGstick is paried with the SLT4 thermostat in <temp_scale>
    When the device is in COOL HOLD mode and the required temperature is set to 5 points above the ambient temperature
    Then the cooler should be off

    Examples: Temperature scale
    |temp_scale|
    |FAHRENHEIT|
    |   CELCIUS|


  @STH_US_RegressionTest @STH_REG_010
  Scenario Outline: STH_REG_010_verify if the protection timer starts for 180 seconds when the cooler is turned on and off repeatedly in heat hold mode
    Given the TGstick is paried with the SLT4 thermostat in <temp_scale>
    When the device is set to COOL HOLD mode and the required temperature is set to 5 points below the ambient temperature 2 times
      Then the cooler should be off
    #Due to sleeps that were used in the case we need a time off of like 15 seconds
      Then the protection timer should be on for 165 seconds

      Examples: Temperature scale
    |temp_scale|
    |FAHRENHEIT|
    |   CELCIUS|






