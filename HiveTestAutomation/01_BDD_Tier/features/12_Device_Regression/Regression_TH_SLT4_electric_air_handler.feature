Feature: Regression test automation of  SLT4 stat at a zigbee level

# These cases automate the associated SLT4 related zigbee cases
# NOTE / IMPORTANT : It is mandatory to set the SLT4 to the correct configuration before attempting to run the tests
# Wiring configurations for this test W1, Y1, Rh, G, C
# The device mode should be selected to ELECTRIC AIR HANDLER and SHOULD BE IN DUAL MODE

  @SLT4_RegressionTest_Electric_handler @SC-CH-MC27
    Scenario Outline: SC-CH-MC27_verify if the user is able to switch to different modes
      Given the TGstick is paired with the SLT4 thermostat and the device is switched to  <temp_scale> scale
      When The stat is set to mode <device_mode>
      Then it should be switched to mode <device_mode>

      Examples: Device Modes
    |temp_scale|device_mode    |
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


  @SLT4_RegressionTest_Electric_handler @SC-UC-02
    Scenario Outline: SC-UC-02_verify if the stat is able to switchg between different temperature Scale
      Given the TGstick is paired with the SLT4 thermostat and the device is switched to  <temp_scale> scale
      Then the temperature scale on the stat should be set to <temp_scale>

      Examples: Temperature scale
      |temp_scale|
      |FAHRENHEIT|
      |CELCIUS   |


  @SLT4_RegressionTest_Electric_handler @SC-MT-21
    Scenario Outline: SC-MT-21_verify if the stat is able to be set to quick cool and heat mode
      Given the TGstick is paired with the SLT4 thermostat and the device is switched to  <temp_scale> scale
      When the device is in <device_mode> mode and the required temperature is set to <number> points <value> the ambient temperature
      Then the <device_state> should be on

      Examples: Device Valid mode transtions
      |temp_scale|value     |device_mode|number|    device_state        |
      |FAHRENHEIT|above     |HEAT_BOOST |5     |HEAT_STAGE_1 FAN_STAGE_1|
      |FAHRENHEIT|below     |COOL_BOOST |5     |COOL_STAGE_1 FAN_STAGE_1|
      |CELCIUS   |above     |HEAT_BOOST |5     |HEAT_STAGE_1 FAN_STAGE_1|
      |CELCIUS   |below     |COOL_BOOST |5     |COOL_STAGE_1 FAN_STAGE_1|


  @SLT4_RegressionTest_Electric_handler @SC-MT-28
    Scenario Outline: SC-MT-28_verify the override values in heat boost and heat hold mode
      Given the TGstick is paired with the SLT4 thermostat and the device is switched to  <temp_scale> scale
      When the device is in <device_mode> mode and the required temperature is set to <number> points <value> the ambient temperature without protection timer validation
      When The heat temperature is overridden by <change> points
      Then The heat temperature should be changed by <change> points

      Examples: Different heat modes
      |temp_scale|value     |device_mode|number|change|
      |FAHRENHEIT|above     |HEAT_BOOST |2     |2     |
      |FAHRENHEIT|above     |HEAT HOLD  |2     |2     |
      |CELCIUS   |above     |HEAT_BOOST |2     |2     |
      |CELCIUS   |above     |HEAT HOLD  |2     |2     |


  @SLT4_RegressionTest_Electric_handler @SC-MT-29
    Scenario Outline: SC-MT-29_verify the override values in cool boost and cool hold mode
      Given the TGstick is paired with the SLT4 thermostat and the device is switched to  <temp_scale> scale
      When the device is in <device_mode> mode and the required temperature is set to <number> points <value> the ambient temperature without protection timer validation
      When The cool temperature is overridden by <change> points
      Then The cool temperature should be changed by <change> points

      Examples: Different cooling modes
      |temp_scale|value     |device_mode|number|change|
      |FAHRENHEIT|below     |COOL_BOOST |2     |2     |
      |FAHRENHEIT|below     |COOL HOLD  |2     |2     |
      |CELCIUS   |below     |COOL_BOOST |2     |2     |
      |CELCIUS   |below     |COOL HOLD  |2     |2     |


  @SLT4_RegressionTest_Electric_handler @SC-PT-03
    Scenario Outline: SC-PT-03_verify the protection timer functionality
      Given the TGstick is paired with the SLT4 thermostat and the device is switched to  <temp_scale> scale
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


    @SLT4_RegressionTest_Electric_handler @SC-MT-20
      Scenario Outline: SC-MT-20_verify when the device is in dual mode , The temperature values can be set properly
        Given the TGstick is paired with the SLT4 thermostat and the device is switched to  <temp_scale> scale
        When the device is set to dual mode <mode> , with heating set to <heat_temp> and cooling set to <cool_temp>
        Then The heat temperature should be <heat_temp>
        Then The cool temperature should be <cool_temp>

        Examples: Different heat modes
        |temp_scale|mode     |heat_temp|cool_temp|
        |CELCIUS   |DUAL HOLD|22       |26       |


    @SLT4_RegressionTest_Electric_handler @SC-MT-23
      Scenario Outline: SC-MT-23_verify if the device is able to toggle from Quick heat to Quick cool mode
        Given the TGstick is paired with the SLT4 thermostat and the device is switched to  <temp_scale> scale
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


    @SLT4_RegressionTest_Electric_handler @SC-MT-22
      Scenario Outline: SC-MT-22_verify if the user is able to change the boost duration
        Given the TGstick is paired with the SLT4 thermostat and the device is switched to  <temp_scale> scale
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



    @SLT4_RegressionTest_Electric_handler @SC-MT-FT-12
      Scenario Outline: SC-MT-FT-12_validate the different device fan modes
        Given the TGstick is paired with the SLT4 thermostat and the device is switched to  <temp_scale> scale
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



  @SLT4_RegressionTest_Electric_handler @SC-MT-34
    Scenario Outline: SC-MT-34_validate verify if the device is able to toggle to different modes and back to the original mode without a set point
      Given the TGstick is paired with the SLT4 thermostat and the device is switched to  <temp_scale> scale
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



  @SLT4_RegressionTest_Electric_handler @SC-DT-02
    Scenario Outline: SC-DT-02_validate if the user is able to set the device name on the screen
      Given the TGstick is paired with the SLT4 thermostat and the device is switched to  <temp_scale> scale
      When the device name is set to <name>
      Then the device name should be set to <name>

      Examples: Device name
      |temp_scale|name       |
      |FAHRENHEIT|test_device|
      |CELCIUS   |test_device|


  @SLT4_RegressionTest_Electric_handler @SC-MT-24
    Scenario Outline: SC-MT-24_validate When Quick Cool while already active on stat,the latest temperature should be overridden on stat
      Given the TGstick is paired with the SLT4 thermostat and the device is switched to  <temp_scale> scale
      When the device is set to COOL HOLD mode with 5 points below the ambient temperature and is set to COOL_BOOST with 3 points below the ambient temperature
      Then The set cooling temperature should be overridden in the stat

      Examples: Device temperature scale

      |temp_scale|
      |FAHRENHEIT|
      |CELCIUS   |


  @SLT4_RegressionTest_Electric_handler @SC-MT-25
    Scenario Outline: SC-MT-25_validate When Quick heat while already active on stat,the latest temperature should be overridden on stat
      Given the TGstick is paired with the SLT4 thermostat and the device is switched to  <temp_scale> scale
      When the device is set to HEAT HOLD mode with 5 points above the ambient temperature and is set to HEAT_BOOST with 3 points above the ambient temperature
      Then The set heating temperature should be overridden in the stat

      Examples: Device temperature scale

      |temp_scale|
      |FAHRENHEIT|
      |CELCIUS   |


  @SLT4_RegressionTest_Electric_handler @SC-MT-26
    Scenario Outline: SC-MT-26_validate stat should return to the previous mode once quick heat/ cool is completed
      Given the TGstick is paired with the SLT4 thermostat and the device is switched to  <temp_scale> scale
      When the device is in <initial_device_mode> mode and the required temperature is set to <initial_points> points <initial_temp_change_mode> the ambient temperature
      When the device is in <device_mode> mode and the required temperature is set to <temp_points> points <temp_change_mode> the ambient temperature for <duration> minutes
      When After the duration of <duration> minutes
      Then the stat should return to the previous state

      Examples: Device modes of operation

      |initial_device_mode|initial_points|initial_temp_change_mode|temp_scale|device_mode|temp_points|temp_change_mode|duration|
      |       HEAT HOLD   |5             |above                   |FAHRENHEIT|COOL_BOOST |12         |below           |2       |
      |       COOL HOLD   |7             |below                   |FAHRENHEIT|COOL_BOOST |12         |below           |2       |
      |       HEAT HOLD   |5             |above                   |FAHRENHEIT|HEAT_BOOST |12         |above           |2       |
      |       COOL HOLD   |5             |below                   |FAHRENHEIT|HEAT_BOOST |12         |above           |2       |


  @SLT4_RegressionTest_Electric_handler @SC-MT-27
    Scenario Outline: SC-MT-27_validate stat should return to the previous dual hold when quick heat / cool is completed
      Given the TGstick is paired with the SLT4 thermostat and the device is switched to  <temp_scale> scale
      When the device is set to dual mode DUAL HOLD , with heating set to 22 and cooling set to 26
      When the device is in <device_mode> mode and the required temperature is set to <temp_points> points <temp_change_mode> the ambient temperature for <duration> minutes
      When After the duration of <duration> minutes
      Then the stat should return to the previous state

      Examples: Device modes of operation

      |temp_scale|device_mode|temp_points|temp_change_mode|duration|
      |CELCIUS   |COOL_BOOST |5          |below           |2       |
      |FAHRENHEIT|HEAT_BOOST |5          |above           |2       |


    @SLT4_RegressionTest_Electric_handler @SC-MT-30
      Scenario Outline: SC-MT-30_validate stat should return to the previous dual schedule when quick heat / cool is completed
        Given the TGstick is paired with the SLT4 thermostat and the device is switched to  <temp_scale> scale
        When The stat is set to mode DUAL SCHEDULE
        When the device is in <device_mode> mode and the required temperature is set to <temp_points> points <temp_change_mode> the ambient temperature for <duration> minutes
        When After the duration of <duration> minutes
        Then the stat should return to the previous state

        Examples: Device modes of operation

        |temp_scale|device_mode|temp_points|temp_change_mode|duration|
        |CELCIUS   |COOL_BOOST |5          |below           |2       |
        |FAHRENHEIT|HEAT_BOOST |5          |above           |2       |





